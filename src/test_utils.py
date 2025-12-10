from textnode import TextNode, TextType
from utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)
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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "This is an image ![alt text](image.png)"
        expected = [("alt text", "image.png")]

        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "One ![alt1](url1.png) and two ![alt2](url2.jpg)."
        expected = [("alt1", "url1.png"), ("alt2", "url2.jpg")]

        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "No images here!"
        expected = []

        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_brackets_and_parentheses(self):
        text = "Edge ![a [b]](c(1).png) cases"
        expected = [("a [b]", "c(1).png")]

        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_empty_alt_and_url(self):
        text = "![](a.png) and ![alt]() and ![]()"
        expected = [("", "a.png"), ("alt", ""), ("", "")]

        self.assertEqual(extract_markdown_images(text), expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "This is a [link text](http://example.com)"
        expected = [("link text", "http://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "First [one](1.html), second [two](2.html)."
        expected = [("one", "1.html"), ("two", "2.html")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "There are no links here!"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_ignores_images(self):
        text = "This is not a link: ![image alt](img.png), but [yes](ok.html)."
        expected = [("yes", "ok.html")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_brackets_and_parentheses(self):
        text = "Edge [a [b]](c(1).html) cases"
        expected = [("a [b]", "c(1).html")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_empty_text_and_url(self):
        text = "Empty text: [](), valid: [abc](http://)"
        expected = [("", ""), ("abc", "http://")]
        self.assertEqual(extract_markdown_links(text), expected)


import unittest


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "A simple ![cat](cat.png) test.",
            TextType.PLAIN,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("A simple ", TextType.PLAIN),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" test.", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        node = TextNode(
            "Here is ![one](1.png) and ![two](2.png).",
            TextType.PLAIN,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Here is ", TextType.PLAIN),
            TextNode("one", TextType.IMAGE, "1.png"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("two", TextType.IMAGE, "2.png"),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)

    def test_image_with_text_before_and_after(self):
        node = TextNode(
            "Start ![pic](image.jpg) end",
            TextType.PLAIN,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Start ", TextType.PLAIN),
            TextNode("pic", TextType.IMAGE, "image.jpg"),
            TextNode(" end", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)

    def test_no_image_returns_same_node(self):
        node = TextNode("Just plain text.", TextType.PLAIN)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_non_plain_node_unchanged(self):
        node = TextNode("alt text", TextType.IMAGE, "url.png")
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_image_at_start_and_end(self):
        node = TextNode("![start](s.png) in the middle ![end](e.png)", TextType.PLAIN)
        result = split_nodes_image([node])
        expected = [
            TextNode("start", TextType.IMAGE, "s.png"),
            TextNode(" in the middle ", TextType.PLAIN),
            TextNode("end", TextType.IMAGE, "e.png"),
        ]
        self.assertEqual(result, expected)

    def test_empty_string(self):
        node = TextNode("", TextType.PLAIN)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "Visit [OpenAI](https://openai.com) here.",
            TextType.PLAIN,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Visit ", TextType.PLAIN),
            TextNode("OpenAI", TextType.LINK, "https://openai.com"),
            TextNode(" here.", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        node = TextNode(
            "[One](1.html), [Two](2.html)",
            TextType.PLAIN,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("One", TextType.LINK, "1.html"),
            TextNode(", ", TextType.PLAIN),
            TextNode("Two", TextType.LINK, "2.html"),
        ]
        self.assertEqual(result, expected)

    def test_link_with_text_before_after(self):
        node = TextNode(
            "Prefix [linked](url) suffix",
            TextType.PLAIN,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Prefix ", TextType.PLAIN),
            TextNode("linked", TextType.LINK, "url"),
            TextNode(" suffix", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)

    def test_no_link_returns_same_node(self):
        node = TextNode("plain with no link", TextType.PLAIN)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_non_plain_node_unchanged(self):
        node = TextNode("click me", TextType.LINK, "url")
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_link_and_image(self):
        node = TextNode(
            "A link: [foo](bar.html) and an image: ![x](y.png)", TextType.PLAIN
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("A link: ", TextType.PLAIN),
            TextNode("foo", TextType.LINK, "bar.html"),
            TextNode(" and an image: ![x](y.png)", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)

    def test_link_at_start_and_end(self):
        node = TextNode("[start](s) middle [end](e)", TextType.PLAIN)
        result = split_nodes_link([node])
        expected = [
            TextNode("start", TextType.LINK, "s"),
            TextNode(" middle ", TextType.PLAIN),
            TextNode("end", TextType.LINK, "e"),
        ]
        self.assertEqual(result, expected)

    def test_empty_string(self):
        node = TextNode("", TextType.PLAIN)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text_node(self):
        text = "This is just plain text."
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is just plain text.", TextType.PLAIN)]
        self.assertEqual(nodes, expected)

    def test_text_with_image(self):
        text = "Text with ![kitty](cat.png) inline."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("kitty", TextType.IMAGE, "cat.png"),
            TextNode(" inline.", TextType.PLAIN),
        ]
        self.assertEqual(nodes, expected)

    def test_text_with_link(self):
        text = "Here is a [website](https://example.com)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Here is a ", TextType.PLAIN),
            TextNode("website", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertEqual(nodes, expected)

    def test_text_with_bold_and_italic_and_code(self):
        text = "It is *italic*, **bold**, and `code`."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("It is ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(", and ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertEqual(nodes, expected)

    def test_text_with_multiple_features(self):
        text = "See ![img](u.png), *em*, [l](u), and `c`."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("See ", TextType.PLAIN),
            TextNode("img", TextType.IMAGE, "u.png"),
            TextNode(", ", TextType.PLAIN),
            TextNode("em", TextType.ITALIC),
            TextNode(", ", TextType.PLAIN),
            TextNode("l", TextType.LINK, "u"),
            TextNode(", and ", TextType.PLAIN),
            TextNode("c", TextType.CODE),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertEqual(nodes, expected)

    def test_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        expected = []
        self.assertEqual(nodes, expected)

    def test_removes_empty_nodes_from_split(self):
        text = "Here is `code` and plain"
        nodes = text_to_textnodes(text)
        # No empty text nodes should be present
        for n in nodes:
            self.assertNotEqual(n.text, "")

    def test_text_with_underscore_italic(self):
        text = "This _is_ important"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This ", TextType.PLAIN),
            TextNode("is", TextType.ITALIC),
            TextNode(" important", TextType.PLAIN),
        ]
        self.assertEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
