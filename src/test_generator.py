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

        self.assertEqual(
            html,
            "<div><h1>Hi test!</h1><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists_and_quote(self):
        md = """
        - first *item*
        - second with a [link](url)

        1. uno
        2. dos

        > quoted line
        > and _more_ quote
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<ul><li>first <i>item</i></li>"
            '<li>second with a <a href="url">link</a></li></ul>'
            "<ol><li>uno</li><li>dos</li></ol>"
            "<blockquote>quoted line and <i>more</i> quote</blockquote>"
            "</div>",
        )

    def test_heading_levels_and_inline(self):
        md = """
        ## Heading with **bold**

        Regular paragraph with ![img](pic.png)
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h2>Heading with <b>bold</b></h2>"
            '<p>Regular paragraph with <img src="pic.png" alt="img"></img></p>'
            "</div>",
        )


if __name__ == "__main__":
    unittest.main()
