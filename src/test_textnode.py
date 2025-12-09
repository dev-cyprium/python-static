import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_same(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("World", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_different_text_type(self):
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_url_same(self):
        node = TextNode("link", TextType.LINK, "http://url")
        node2 = TextNode("link", TextType.LINK, "http://url")
        self.assertEqual(node, node2)

    def test_eq_with_url_different(self):
        node = TextNode("link", TextType.LINK, "http://url1")
        node2 = TextNode("link", TextType.LINK, "http://url2")
        self.assertNotEqual(node, node2)

    def test_eq_url_vs_no_url(self):
        node = TextNode("link", TextType.LINK, "http://url")
        node2 = TextNode("link", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_eq_to_non_textnode(self):
        node = TextNode("test", TextType.PLAIN)
        self.assertNotEqual(node, "test")

    def test_repr(self):
        node = TextNode("foo", TextType.ITALIC, "bar")
        self.assertEqual(repr(node), "TextNode(foo, italic, bar)")
        node2 = TextNode("hello", TextType.PLAIN)
        self.assertEqual(repr(node2), "TextNode(hello, plain, None)")


if __name__ == "__main__":
    unittest.main()
