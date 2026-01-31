from textnode import TextNode, TextType
import re 

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:    
            parts = old_node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("unmatched delimiter")
            for i in range(len(parts)):
                part = parts[i]
                if part == "":
                    continue 
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
                    
            
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches 
        
def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        images = extract_markdown_images(old_node.text)
        
        if images == []:
            new_nodes.append(old_node)
            continue

        # Work with the text of this node
        text = old_node.text

        # Handle each image in this text
        for alt, url in images:
            image_markdown = f"![{alt}]({url})"
            parts = text.split(image_markdown, 1)
            before = parts[0]
            after = parts[1] if len(parts) > 1 else ""

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            # Continue processing any remaining text after this image
            text = after

        # After all images, if there is leftover text, add it
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        links = extract_markdown_links(old_node.text)
        if links == []:
            new_nodes.append(old_node)
            continue

        # Work with the text of this node
        text = old_node.text

        # Handle each image in this text
        for alt, url in links:
            link_markdown = f"[{alt}]({url})"
            parts = text.split(link_markdown, 1)
            before = parts[0]
            after = parts[1] if len(parts) > 1 else ""

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.LINK, url))

            # Continue processing any remaining text after this image
            text = after

        # After all images, if there is leftover text, add it
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)

    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    new_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            new_blocks.append(block)
    return new_blocks


    
    