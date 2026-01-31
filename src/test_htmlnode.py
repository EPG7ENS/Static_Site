import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        node = HTMLNode(
            tag="a",
            value="link",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )
        
    def test_props_to_html_none(self):
        node = HTMLNode(tag="p", value="hello", props=None)  # Arrange
        result = node.props_to_html()                        # Act
        self.assertEqual(result, "")                         # Assert
            
    def test_props_to_html_empty_dict(self):
        node = HTMLNode(tag="p", value="hello", props={})  # Arrange
        result = node.props_to_html()                      # Act
        self.assertEqual(result, "")                       # Assert
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a_with_href(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        

if __name__ == "__main__":
    unittest.main()