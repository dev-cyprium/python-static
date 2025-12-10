import unittest

from generator import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
        # Hi test!

        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()

        print("HTML ~>")
        print(html)
        print(">> END HTML")

        self.assertEqual(
            html,
            "<div><h1>Hi test!</h1><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
