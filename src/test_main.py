import unittest

from markdown_to_html_node import text_node_to_html_node, text_to_textnodes, markdown_to_blocks
from main import extract_title
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode



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
        

class TestTextToTextNodes(unittest.TestCase):

    def test_text1(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")])

class TestMarkdownToHTML(unittest.TestCase):

    def test_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("This is ", TextType.TEXT),
                            TextNode("bold", TextType.BOLD),
                            TextNode(" text", TextType.TEXT)])
    
    def test_italic(self):
        text = "This is *italic* text"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("This is ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" text", TextType.TEXT)])
        
    def test_code(self):
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("This is ", TextType.TEXT),
                            TextNode("code", TextType.CODE),
                            TextNode(" text", TextType.TEXT)])

    def test_invalid_bold(self):
        text = "This is **text with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        with self.assertRaises(ValueError) as context:
            text_to_textnodes(text)
        self.assertEqual(str(context.exception), "invalid markdown, formatted section not closed")

    def test_invalid_italic(self):
        text = "This is *text with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        with self.assertRaises(ValueError) as context:
            text_to_textnodes(text)
        self.assertEqual(str(context.exception), "invalid markdown, formatted section not closed")
    
    def test_invalid_code(self):
        text = "This is text with an *italic* word and a `code block and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        with self.assertRaises(ValueError) as context:
            text_to_textnodes(text)
        self.assertEqual(str(context.exception), "invalid markdown, formatted section not closed")

    def test_nested_invalid(self):
        text = "This is **bold with *italic* inside**"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("This is ", TextType.TEXT), 
                                 TextNode("bold with *italic* inside", TextType.BOLD)])

    def test_multiple_links(self):
        text = "[link1](url1) normal text [link2](url2)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("link1", TextType.LINK, "url1"), 
                                 TextNode(" normal text ", TextType.TEXT), 
                                 TextNode("link2", TextType.LINK, "url2")])
        
    def test_invalid_link(self):
        text = "[link1](url1) normal text [link2(url2)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("link1", TextType.LINK, "url1"), 
                                 TextNode(" normal text [link2(url2)", TextType.TEXT)])
        
class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_block_text1(self):
        markdown = "This is a text block\n\nThis is another text block"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["This is a text block", "This is another text block"])

    def test_markdown_block_text2(self):
        markdown = "This is a text block \n\nThis is another text block "
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["This is a text block", "This is another text block"])

    def test_markdown_block_text3(self):
        markdown = "This is a text block\n\n\nThis is another text block"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["This is a text block", "This is another text block"])

    def test_markdown_block_text4(self):
        markdown = "This is a text block\n\n\n\nThis is another text block"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["This is a text block", "This is another text block"])

    def test_markdown_block_text5(self):
        markdown = "# This is a text block\n\n* This is another text block\n* This is another text block\n* This is another text block\n\n "
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["# This is a text block", "* This is another text block\n* This is another text block\n* This is another text block"])

    def test_markdown_block_text6(self):
        markdown = "This is a block of text"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["This is a block of text"])

    def test_markdown_block_text7(self):
        markdown = "This is a **bold block** of text\n"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["This is a **bold block** of text"])

    def test_markdown_block_empty(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, [])

class TestExtractHeading(unittest.TestCase):

    def test_heading1(self):
        markdown = "# Heading"
        heading = extract_title(markdown)
        self.assertEqual(heading, "Heading")

    def test_heading2(self):
        markdown = "Heading"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "Error: no heading found starting with '# '")

    def test_heading3(self):
        markdown = "# Heading\n\nThis is a text block"
        heading = extract_title(markdown)
        self.assertEqual(heading, "Heading")

    def test_heading4(self):
        markdown = "## Heading\n\n"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "Error: no heading found starting with '# '")

    

    

if __name__ == "__main__":
    unittest.main()