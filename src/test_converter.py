import unittest

from src.textnode import TextNode, TextType
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.converter import text_node_to_html_node


class TestConverter(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode(None, "This is a text node"))
    
    def test_text_node_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("b", "This is a text node"))
    
    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("i", "This is a text node"))
    
    def test_text_node_to_html_node_code(self):
        text_node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("code", "This is a text node"))
    
    def test_text_node_to_html_node_link(self):
        text_node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("a", "This is a text node", {"href": "https://www.boot.dev"}))
    
    def test_text_node_to_html_node_image(self):
        text_node = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("img", "", {"alt": "This is a text node", "src": "https://www.boot.dev"}))

    def test_text_node_to_html_node_invalid(self):
        with self.assertRaises(ValueError) as context:
            text_node = TextNode("This is a text node", "invalid")
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Invalid TextType")
        

if __name__ == "__main__":
    unittest.main()