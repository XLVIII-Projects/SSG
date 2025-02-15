import unittest

# from main import text_node_to_html_node, text_to_textnodes, markdown_to_blocks
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_to_html_node import markdown_to_html_node


class MarkdownToHTMLNode(unittest.TestCase):
            
    def test_markdown_to_html_node_text1(self):
        markdown = "This is a text node"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><p>This is a text node</p></div>")

    def test_markdown_to_html_node_heading(self):
        markdown = "###### This is a heading"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><h6>This is a heading</h6></div>")

    def test_markdown_to_html_node_heading2(self):
        markdown = "##### This is a heading"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><h5>This is a heading</h5></div>")
    
    def test_markdown_to_html_node_combinationmarkdown(self):
        markdown = "# This is a heading\n\n```This is a code block```"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><h1>This is a heading</h1><pre><code>This is a code block</code></pre></div>")

    def test_markdown_to_html_node_code(self):
        markdown = "```This is a code block```"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><pre><code>This is a code block</code></pre></div>")

    def test_markdown_to_html_node_unordered_list(self):
        markdown = "* This is a list\n* This is a list\n- This is a list"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><ul><li>This is a list</li><li>This is a list</li><li>This is a list</li></ul></div>")

    def test_markdown_to_html_node_ordered_list(self):
        markdown = "1. This is a list\n2. This is a list\n3. This is a list"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><ol><li>This is a list</li><li>This is a list</li><li>This is a list</li></ol></div>")

    def test_markdown_to_html_node_quote(self):
        markdown = "> This is a quote\n> This is a quote"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><blockquote>This is a quote\nThis is a quote</blockquote></div>")

    def test_markdown_to_html_node_combinationmarkdown2(self):
        markdown = "# This is a **bold** heading\n\nThis is a **bold** text"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><h1>This is a <b>bold</b> heading</h1><p>This is a <b>bold</b> text</p></div>")

    def test_markdown_to_html_node_combinationmarkdown3(self):
        markdown = "* First item\n* Second **bold** item\n- Third *italic* item"
        expected = "<div><ul><li>First item</li><li>Second <b>bold</b> item</li><li>Third <i>italic</i> item</li></ul></div>"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()