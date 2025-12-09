from textnode import TextNode, TextType
from utils import text_node_to_html_node
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


if __name__ == "__main__":
    unittest.main()
