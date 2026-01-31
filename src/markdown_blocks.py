from enum import Enum
from htmlnode import ParentNode
from extra_functions import markdown_to_blocks,text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for tn in text_nodes:
        children.append(text_node_to_html_node(tn))
    return children

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def block_to_block_type(markdown):
    # Look only at the first line for headings
    first_line = markdown.split("\n", 1)[0]

    if first_line.startswith("#"):
        count = 0
        for ch in first_line:
            if ch == "#":
                count += 1
            else:
                break
        if 1 <= count <= 6 and len(first_line) > count and first_line[count] == " ":
            return BlockType.HEADING

    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE

    lines = markdown.split("\n")

    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE

    is_unordered = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST

    is_ordered = True
    expected = 1
    for line in lines:
        prefix = f"{expected}. "
        if not line.startswith(prefix):
            is_ordered = False
            break
        expected += 1
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)
    
def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        lines = block.split("\n")
        paragraph_text = " ".join(lines)
        children = text_to_children(paragraph_text)
        return ParentNode("p", children)

    if block_type == BlockType.HEADING:
        level = 0
        for ch in block:
            if ch == "#":
                level += 1
            else:
                break
        text = block[level + 1 :]
        children = text_to_children(text)
        return ParentNode(f"h{level}", children)

    if block_type == BlockType.CODE:
        # strip the starting "```\n" and ending "```"
        if not (block.startswith("```\n") and block.endswith("```")):
            raise ValueError("invalid code block")
        inner = block[4:-3]  # keep newlines as-is
        raw = TextNode(inner, TextType.TEXT)
        child = text_node_to_html_node(raw)
        code_node = ParentNode("code", [child])
        return ParentNode("pre", [code_node])

    if block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        li_nodes = []
        for line in lines:
            # remove "- " prefix
            item_text = line[2:]
            children = text_to_children(item_text)
            li_nodes.append(ParentNode("li", children))
        return ParentNode("ul", li_nodes)
    
    if block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        li_nodes = []
        for line in lines:
            # split "1. item text" into ["1", "item text"]
            parts = line.split(". ", 1)
            if len(parts) != 2:
                continue  # or raise, but continue is fine for now
            item_text = parts[1]
            children = text_to_children(item_text)
            li_nodes.append(ParentNode("li", children))
        return ParentNode("ol", li_nodes)
    
    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        stripped_lines = []
        for line in lines:
            # remove leading ">" and optional space
            if line.startswith(">"):
                stripped_lines.append(line.lstrip(">").strip())
        # join quote lines with spaces
        content = " ".join(stripped_lines)
        children = text_to_children(content)
        return ParentNode("blockquote", children)
    
    return ParentNode("p", [])