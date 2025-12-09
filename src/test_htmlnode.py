import unittest

from htmlnode import HTMLNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_values(self):
        children = [HTMLNode(tag="span", value="hi")]
        props = {"href": "http://test"}
        node = HTMLNode(tag="a", value="hello", children=children, props=props)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "hello")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "link"})
        self.assertEqual(node.props_to_html(), ' href="link"')

    def test_props_to_html_multiple(self):
        # The order may not be deterministic in < Python 3.7
        node = HTMLNode(props={"href": "url", "class": "foo"})
        html = node.props_to_html()
        self.assertTrue(html.startswith(" "))
        # Both attrs must be present
        self.assertIn('href="url"', html)
        self.assertIn('class="foo"', html)

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("div", "hello", [HTMLNode("span")], {"class": "c"})
        expected = "HTMLNode(tag=div, value=hello, children=[HTMLNode(tag=span, value=None, children=None, props=None)], props={'class': 'c'})"
        self.assertEqual(repr(node), expected)


import unittest

from htmlnode import HTMLNode, LeafNode


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode("p", "Some text", {"class": "cls"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Some text")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"class": "cls"})

    def test_init_no_props(self):
        node = LeafNode("p", "Some text")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Some text")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_with_tag_and_props(self):
        node = LeafNode("b", "bold", {"class": "fancy"})
        # props_to_html should return ' class="fancy"', so the full string is:
        self.assertEqual(node.to_html(), '<b class="fancy">bold</b>')

    def test_to_html_with_tag_no_props(self):
        node = LeafNode("i", "italic")
        # props_to_html should return '', so the full string is:
        self.assertEqual(node.to_html(), "<i>italic</i>")

    def test_to_html_raises_when_value_missing(self):
        node = LeafNode("span", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode("p", "txt", {"id": "x"})
        expected = "HTMLNode(tag=p, value=txt, children=None, props={'id': 'x'})"
        self.assertEqual(repr(node), expected)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "c1")
        child2 = LeafNode("b", "c2")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><span>c1</span><b>c2</b></div>")

    def test_to_html_with_mixed_leaf_and_parent_children(self):
        grandchild = LeafNode("em", "inner")
        child1 = ParentNode("span", [grandchild])
        child2 = LeafNode("strong", "text")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><span><em>inner</em></span><strong>text</strong></div>",
        )

    def test_to_html_with_props(self):
        child = LeafNode("span", "data")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        # The order of props may vary: test using 'in'
        html = parent.to_html()
        self.assertTrue(html.startswith("<div "))
        self.assertIn('class="container"', html)
        self.assertIn('id="main"', html)
        self.assertTrue(html.endswith("></div>") or html.endswith("></div>"))
        self.assertIn("<span>data</span>", html)

    def test_to_html_raises_error_no_tag(self):
        child = LeafNode("p", "child")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_raises_error_no_children(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_raises_error_empty_children(self):
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_repr(self):
        children = [LeafNode("span", "child")]
        node = ParentNode("div", children, {"data": "val"})
        expected_prefix = "HTMLNode(tag=div"
        self.assertTrue(repr(node).startswith(expected_prefix))
        self.assertIn("children=", repr(node))
        self.assertIn("'data': 'val'", repr(node))


if __name__ == "__main__":
    unittest.main()
