import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_not_equal_text(self):
        node = TextNode("hello", TextType.TEXT)
        node2 = TextNode("goodbye", TextType.TEXT)
        self.assertNotEqual(node,node2)
        
    def test_not_equal_text_type(self):
        node = TextNode("hello", TextType.TEXT)
        node2 = TextNode("hello", TextType.BOLD)
        self.assertNotEqual(node,node2)
        
    def test_equal_with_url(self):
        node = TextNode("hello", TextType.TEXT,url = "https://www.youtube.com/watch?v=CB4fvGXl6BU")
        node2 = TextNode("hello", TextType.TEXT, url="https://www.youtube.com/watch?v=CB4fvGXl6BU")
        self.assertEqual(node,node2)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()