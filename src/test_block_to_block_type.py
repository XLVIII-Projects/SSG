import unittest

from block_to_block_type import block_to_block_type


class TestBlockToBlockType(unittest.TestCase):

    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "heading")

    # def test_block_to_block_type_notheading(self):
    #     block = "# # This is a heading"
    #     block_type = block_to_block_type(block)
    #     self.assertEqual(block_type, "paragraph")

    def test_block_to_block_type_code(self):
        block = "```This is a code block```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "code")

    def test_block_to_block_type_notcode(self):
        block = "```This is a code block``"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_block_to_block_type_quote(self):
        block = "> This is a quote\n> This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "quote")

    def test_block_to_block_type_notquote(self):
        block = "> This is a quote\nThis is a not quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_block_to_block_type_unordered_list(self):
        block = "* This is a list\n* This is a list\n- This is a list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "unordered_list")

    def test_block_to_block_type_notunordered_list(self):
        block = "* This is a list\n-This is a not list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a list\n2. This is a list\n3. This is a list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "ordered_list")