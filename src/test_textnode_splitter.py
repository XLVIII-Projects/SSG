import unittest

from textnode_splitter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestSplitNode(unittest.TestCase):
     
    def test_split_texttype_bold(self):
        node = TextNode("This is a **bold** text node", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_node, [TextNode("This is a ", TextType.TEXT), 
                                    TextNode("bold", TextType.BOLD), 
                                    TextNode(" text node", TextType.TEXT)])

    def test_split_texttype_italic(self):
        node = TextNode("This is an *italic* text node", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_node, [TextNode("This is an ", TextType.TEXT), 
                                    TextNode("italic", TextType.ITALIC), 
                                    TextNode(" text node", TextType.TEXT)])

    def test_split_textype_code(self):
        node = TextNode("This is a `code` text node", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_node, [TextNode("This is a ", TextType.TEXT), 
                                    TextNode("code", TextType.CODE), 
                                    TextNode(" text node", TextType.TEXT)])

    def test_split_multiplenodes(self):
        node = [TextNode("This is a `code` text node", TextType.TEXT), TextNode("This is an *italic* text node", TextType.TEXT)]
        new_node = split_nodes_delimiter(node, "*", TextType.ITALIC)
        self.assertEqual(new_node, [TextNode("This is a `code` text node", TextType.TEXT), 
                                    TextNode("This is an ", TextType.TEXT), 
                                    TextNode("italic", TextType.ITALIC), 
                                    TextNode(" text node", TextType.TEXT)])

    def test_split_boldnode(self):
        node = TextNode("**This is a bold text node**", TextType.BOLD)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_node, [TextNode("**This is a bold text node**", TextType.BOLD)])

    def test_multiple_delimiters(self):
        node = TextNode("This is **bold** and **bold again**", TextType.TEXT)   
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_node, [
            TextNode("This is ", TextType.TEXT), 
            TextNode("bold", TextType.BOLD), 
            TextNode(" and ", TextType.TEXT), 
            TextNode("bold again", TextType.BOLD)])
        
    def test_invalid_delimiter(self):
        with self.assertRaises(ValueError) as context:
            node = TextNode("This is a **text node", TextType.TEXT)
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "invalid markdown, formatted section not closed")

class TestMarkdownImg(unittest.TestCase):

    def test_double_img(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extract = extract_markdown_images(text)
        self.assertEqual(extract, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_no_img(self):
        text = "This is text with no images"
        extract = extract_markdown_images(text)
        self.assertEqual(extract, [])

    def test_img_brackets(self):
        text = "This is text with a ![[rick] roll](https://i.(imgur).com/aKaOqIh.gif)"
        extract = extract_markdown_images(text)
        self.assertEqual(extract, [])
     
    def test_double_link(self):
        text = "This is text with a [link](https://www.google.com) and [another link](https://www.facebook.com)"
        extract = extract_markdown_links(text)
        self.assertEqual(extract, [("link", "https://www.google.com"), ("another link", "https://www.facebook.com")])

    def test_empty_string(self):
        text = ""
        extract = extract_markdown_links(text)
        self.assertEqual(extract, [])

    def test_img_without_url(self):
        text = "This is text with a ![alt text]()"
        extract = extract_markdown_images(text)
        self.assertEqual(extract, [("alt text", "")])

    def test_malformed_img(self):
        text = "This is text with a ![link without closure](https://example.com"
        extract = extract_markdown_images(text)
        self.assertEqual(extract, [])

    def test_mixed_links_and_images(self):
        text = "Text with ![image](https://example.com/image.jpg) and [link](https://example.com)"
        extract_images = extract_markdown_images(text)
        self.assertEqual(extract_images, [("image", "https://example.com/image.jpg")])

    def test_mixed_links_and_images2(self):
        text = "Text with ![image](https://example.com/image.jpg) and [link](https://example.com)"
        extract_images = extract_markdown_links(text)
        self.assertEqual(extract_images, [("link", "https://example.com")])

class TestSplitNodesImageLink(unittest.TestCase):

    def test_single_image(self):
        node = TextNode("This is an image: ![image](https://example.com/image.jpg) that I love", TextType.TEXT)
        new_node = split_nodes_image([node])
        self.assertEqual(new_node, [
            TextNode("This is an image: ", TextType.TEXT), 
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"), 
            TextNode(" that I love", TextType.TEXT)])
        
    def test_multiple_images(self):
        node = TextNode("This is an image: ![image](https://example.com/image.jpg) that I love, and also ![another image](https://example.com/image2.jpg) fabulous!", TextType.TEXT)
        new_node = split_nodes_image([node])
        self.assertEqual(new_node, [
            TextNode("This is an image: ", TextType.TEXT), 
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"), 
            TextNode(" that I love, and also ", TextType.TEXT),
            TextNode("another image", TextType.IMAGE, "https://example.com/image2.jpg"),
            TextNode(" fabulous!", TextType.TEXT)])

    def test_sinlge_link(self):
        node = TextNode("This is a link: [link](https://example.com)", TextType.TEXT)
        new_node = split_nodes_link([node])
        self.assertEqual(new_node, [
            TextNode("This is a link: ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com")])

    def test_multiple_links(self):
        node = TextNode("This is a link: [link](https://example.com) and [another link](https://example.com)", TextType.TEXT)  
        new_node = split_nodes_link([node])
        self.assertEqual(new_node, [
            TextNode("This is a link: ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another link", TextType.LINK, "https://example.com")])

    def test_mixed_links_and_images(self):
        node = TextNode("This is a link: [link](https://example.com) and an image ![image](https://example.com/image.jpg)", TextType.TEXT)
        new_node = split_nodes_link([node])
        self.assertEqual(new_node, [
            TextNode("This is a link: ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and an image ![image](https://example.com/image.jpg)", TextType.TEXT)])

    def test_start_link(self):
        node = TextNode("[link](https://example.com) and an image ![image](https://example.com/image.jpg)", TextType.TEXT)
        new_node = split_nodes_link([node])
        self.assertEqual(new_node, [
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and an image ![image](https://example.com/image.jpg)", TextType.TEXT)])
        
    def test_no_link(self):
        node = TextNode("This is a text node", TextType.TEXT)
        new_node = split_nodes_link([node])
        self.assertEqual(new_node, [TextNode("This is a text node", TextType.TEXT)])

    def test_multiple_nodes(self):
        node = [TextNode("This is a link: [link](https://example.com)", TextType.TEXT), 
                TextNode("This is an image: ![image](https://example.com/image.jpg)", TextType.TEXT)]
        new_node = split_nodes_link(node)
        self.assertEqual(new_node, [
            TextNode("This is a link: ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode("This is an image: ![image](https://example.com/image.jpg)", TextType.TEXT)])
        
    def test_wrong_syntax(self):
        node = TextNode("This is a link: [link](https://example.com", TextType.TEXT)
        new_node = split_nodes_link([node])
        self.assertEqual(new_node, [TextNode("This is a link: [link](https://example.com", TextType.TEXT)])

    def test_empty_link(self):
        node = TextNode("This is a link: [](https://example.com) et voila!", TextType.TEXT)
        new_node = split_nodes_link([node])
        self.assertEqual(new_node, [TextNode("This is a link: ", TextType.TEXT), 
                                    TextNode(" et voila!", TextType.TEXT)])
    
    def test_empty_image(self):
        node = TextNode("This is an image: ![]() et voila!", TextType.TEXT)
        new_node = split_nodes_image([node])
        self.assertEqual(new_node, [TextNode("This is an image: ", TextType.TEXT), 
                                    TextNode(" et voila!", TextType.TEXT)])

    def test_sequential_links(self):
        node = TextNode("[link](https://example.com)[another link](https://example.com)", TextType.TEXT)
        new_node = split_nodes_link([node])
        self.assertEqual(new_node, [
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode("another link", TextType.LINK, "https://example.com")])    



if __name__ == "__main__":
    unittest.main()