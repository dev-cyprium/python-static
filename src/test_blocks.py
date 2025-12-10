import unittest
from blocks import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "#Heading (no space so not heading)"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\ncode here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "```python\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "```\nnot closed"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote(self):
        block = "> this is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "> quote1\n> quote2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = ">quote without space"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "> one\nnot a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- item 1\n- item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "- first"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "-item without space\n- item2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "- item\nnot a list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1. one"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1. first\n2.invalid"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "2. should not match"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "Just a paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "     \n  "
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "\nhello"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "\n\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
