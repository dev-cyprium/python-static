from textnode import TextNode, TextType
from utils import split_nodes_delimiter, text_node_to_html_node
import unittest


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_plain_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_bold_text(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_italic_text(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_code_text(self):
        node = TextNode("print('code')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('code')")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_link_text(self):
        node = TextNode("link-text", TextType.LINK, url="http://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "link-text")
        self.assertIsNone(html_node.children)
        self.assertEqual(html_node.props, {"href": "http://example.com"})

    def test_image(self):
        node = TextNode("Example image", TextType.IMAGE, url="http://img.url/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIsNone(html_node.children)
        self.assertEqual(
            html_node.props, {"src": "http://img.url/img.png", "alt": "Example image"}
        )

    def test_plain_text2(self):
        node = TextNode("Just plain", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Just plain")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_unexpected_text_type_raises(self):
        class DummyType:
            pass

        node = TextNode("oops", DummyType())
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_backticks_single_pair(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.PLAIN,
        )

        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]

        self.assertEqual(new_nodes, expected)

    def test_no_delimiter_returns_same_plain_node(self):
        node = TextNode("Just some plain text", TextType.PLAIN)

        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(new_nodes, [node])

    def test_non_plain_nodes_are_unchanged(self):
        node_code = TextNode("already code", TextType.CODE)
        node_bold = TextNode("already bold", TextType.BOLD)

        new_nodes = split_nodes_delimiter([node_code, node_bold], "`", TextType.CODE)

        self.assertEqual(new_nodes, [node_code, node_bold])

    def test_multiple_delimited_sections_in_one_node(self):
        node = TextNode(
            "Here is `code1` and here is `code2`.",
            TextType.PLAIN,
        )

        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("Here is ", TextType.PLAIN),
            TextNode("code1", TextType.CODE),
            TextNode(" and here is ", TextType.PLAIN),
            TextNode("code2", TextType.CODE),
            TextNode(".", TextType.PLAIN),
        ]

        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_start_and_end(self):
        node = TextNode(
            "`start` and `end`",
            TextType.PLAIN,
        )

        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("start", TextType.CODE),
            TextNode(" and ", TextType.PLAIN),
            TextNode("end", TextType.CODE),
        ]

        self.assertEqual(new_nodes, expected)

    def test_unmatched_delimiter_raises(self):
        node = TextNode(
            "This has an `unclosed code section",
            TextType.PLAIN,
        )

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    # ---------- Other delimiters ----------

    def test_italic_with_single_asterisk(self):
        node = TextNode(
            "This is *italic* text",
            TextType.PLAIN,
        )

        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN),
        ]

        self.assertEqual(new_nodes, expected)

    def test_bold_with_double_asterisk(self):
        node = TextNode(
            "This is **bold** text",
            TextType.PLAIN,
        )

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
        ]

        self.assertEqual(new_nodes, expected)

    def test_italic_with_underscore(self):
        node = TextNode(
            "Some _italic_ word",
            TextType.PLAIN,
        )

        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        expected = [
            TextNode("Some ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.PLAIN),
        ]

        self.assertEqual(new_nodes, expected)

    def test_custom_delimiter_tilde(self):
        node = TextNode(
            "Custom ~highlight~ syntax",
            TextType.PLAIN,
        )

        new_nodes = split_nodes_delimiter([node], "~", TextType.CODE)

        expected = [
            TextNode("Custom ", TextType.PLAIN),
            TextNode("highlight", TextType.CODE),
            TextNode(" syntax", TextType.PLAIN),
        ]

        self.assertEqual(new_nodes, expected)

    def test_mixed_plain_and_non_plain_nodes(self):
        nodes = [
            TextNode("This is *italic*", TextType.PLAIN),
            TextNode("no split here", TextType.CODE),
        ]

        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)

        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(
                "", TextType.PLAIN
            ),  # if your implementation skips empties, adjust
            TextNode("no split here", TextType.CODE),
        ]

        # If your implementation *skips* empty strings, then drop that empty node:
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode("no split here", TextType.CODE),
        ]

        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
