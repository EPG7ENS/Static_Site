from extra_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_links, markdown_to_blocks
from textnode import TextNode, TextType
import unittest


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_code(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(3, len(result))
        self.assertEqual("This is ", result[0].text)
        self.assertEqual(TextType.TEXT, result[0].text_type)
        # etc...

    def test_split_nodes_bold(self):
        node = TextNode("a **bold** word", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(3, len(result))
        self.assertEqual("bold", result[1].text)
        self.assertEqual(TextType.BOLD, result[1].text_type)

    def test_split_nodes_ignores_non_text(self):
        text_node = TextNode("no *markdown* here", TextType.TEXT)
        bold_node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([text_node, bold_node], "*", TextType.ITALIC)
        self.assertIs(bold_node, result[-1])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )
        
    def test_split_images_simple(self):
        node = TextNode(
        "Hi ![img](https://example.com/img.png) there",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("Hi ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" there", TextType.TEXT),
        ],
        new_nodes,
        )
        
    def test_split_links_simple(self):
        node = TextNode(
            "Go to [Boot.dev](https://www.boot.dev) now",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" now", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )