import re
from textnode import TextType, TextNode
from htmlnode import LeafNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown: unclosed delimiter")

        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(((?:[^\(\)]|\([^\(\)]*\))*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"(?<!\!)\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(((?:[^\(\)]|\([^\(\)]*\))*)\)"
    return re.findall(pattern, text)


def text_node_to_html_node(text_node):

    match text_node.text_type:
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case _:
            raise ValueError(f"Unexpected TextType: {text_node.text_type}")
