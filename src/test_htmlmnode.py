import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_noteq(self):
        link_node = HTMLNode("link", "value", None, {"href": "https://www.boot.dev"})
        p_node = HTMLNode("paragraph", None, [link_node], None)
        self.assertNotEqual(link_node, p_node)
    
    def test_eq(self):
        link_node = HTMLNode("link", "value", None, {"href": "https://www.boot.dev"})
        link_node2 = HTMLNode("link", "value", None, {"href": "https://www.boot.dev"})
        self.assertEqual(link_node, link_node2)

    def test_props_to_html(self):
        link_node = HTMLNode("tag", "value", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(link_node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_none(self):
        link_node = HTMLNode("tag", "value", None, None)
        self.assertEqual(link_node.props_to_html(), "")

    #test leaf node
    def test_leafnode(self):
        leaf_node = LeafNode("a", "Click here!", {"href": "https://www.google.com"})
        self.assertEqual(leaf_node.to_html(), '<a href="https://www.google.com">Click here!</a>')

    def test_leafnode_eq(self):
        leaf_node = LeafNode("a", "Click here!", {"href": "https://www.google.com"})
        leaf_node2 = LeafNode("a", "Click here!", {"href": "https://www.google.com"})
        self.assertEqual(leaf_node, leaf_node2)

    def test_leafnode_noteq(self):
        leaf_node = LeafNode("a", "Click here!", {"href": "https://www.google.com"})
        leaf_node2 = LeafNode("a", "Click here!", {"href": "https://www.boot.dev"})
        self.assertNotEqual(leaf_node, leaf_node2)

    #test parent node
    def test_mult_children(self):
        link_node = [LeafNode("b", "Bold text"), LeafNode("a", "Click here!", {"href": "https://www.google.com"})]
        p_node = ParentNode("p", link_node)
        self.assertEqual(p_node.to_html(), '<p><b>Bold text</b><a href="https://www.google.com">Click here!</a></p>')
    
    def test_parentnode_eq(self):
        link_node = [LeafNode("b", "Bold text"), LeafNode("a", "Click here!", {"href": "https://www.google.com"})]
        link_node2 = [LeafNode("b", "Bold text"), LeafNode("a", "Click here!", {"href": "https://www.google.com"})]
        p_node = ParentNode("p", link_node)
        p_node2 = ParentNode("p", link_node2)
        self.assertEqual(p_node, p_node2)

    def test_parentnode_noteq(self):    
        link_node = [LeafNode("b", "Bold text"), LeafNode("a", "Click here!", {"href": "https://www.google.com"})]
        link_node2 = [LeafNode("b", "Bold text"), LeafNode("a", "Click here!", {"href": "https://www.boot.dev"})]
        p_node = ParentNode("p", link_node)
        p_node2 = ParentNode("p", link_node2)
        self.assertNotEqual(p_node, p_node2)

    def test_nested_parentnode(self):
        link_node = [LeafNode("b", "Bold text"), LeafNode("a", "Click here!", {"href": "https://www.google.com"})]
        p_node = ParentNode("p", link_node)
        p_node2 = ParentNode("div", [p_node])
        p_node3 = ParentNode("3", [p_node2])
        self.assertEqual(p_node3.to_html(), '<3><div><p><b>Bold text</b><a href="https://www.google.com">Click here!</a></p></div></3>')

    def test_no_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("p", None)
        self.assertEqual(str(context.exception), "ParentNode must have children")

if __name__ == "__main__":
    unittest.main()
    # TestHTMLNode('test_no_children').debug()
    # test = TestHTMLNode('test_no_children')
    # test.debug()
