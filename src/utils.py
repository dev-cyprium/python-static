import re
from textnode import TextType, TextNode
from htmlnode import LeafNode


def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    raw_blocks = re.split(r"(?:\r?\n){2,}", markdown)
    blocks = []
    for block in raw_blocks:
        lines = block.splitlines()
        stripped_lines = [line.strip() for line in lines]
        stripped_lines = [line for line in stripped_lines if line != ""]

        if not stripped_lines:
            continue

        is_unordered = all(line.startswith("- ") for line in stripped_lines)
        is_ordered = all(re.match(r"^\d+\. ", line) for line in stripped_lines)

        if is_unordered or is_ordered:
            blocks.append("\n".join(stripped_lines))
        else:
            blocks.append("\n".join(stripped_lines))
    return blocks


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)

    nodes = [node for node in nodes if node.text != ""]

    return nodes


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


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue

        # Use re.finditer to get positions of the images in the text
        pattern = r"!\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(((?:[^\(\)]|\([^\(\)]*\))*)\)"
        matches = list(re.finditer(pattern, text))

        last_index = 0
        for match, (alt_text, url) in zip(matches, images):
            start, end = match.start(), match.end()

            # Text before the image
            if start > last_index:
                before_text = text[last_index:start]
                if before_text:
                    new_nodes.append(TextNode(before_text, TextType.PLAIN))

            # Image node itself
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            last_index = end

        # Remaining text after the last image
        if last_index < len(text):
            remaining = text[last_index:]
            if remaining:
                new_nodes.append(TextNode(remaining, TextType.PLAIN))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(node)
            continue

        # Use re.finditer to get positions of the links in the text
        pattern = (
            r"(?<!\!)\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(((?:[^\(\)]|\([^\(\)]*\))*)\)"
        )
        matches = list(re.finditer(pattern, text))

        last_index = 0
        for match, (link_text, url) in zip(matches, links):
            start, end = match.start(), match.end()

            # Text before the link
            if start > last_index:
                before_text = text[last_index:start]
                if before_text:
                    new_nodes.append(TextNode(before_text, TextType.PLAIN))

            # The link node itself
            new_nodes.append(TextNode(link_text, TextType.LINK, url))

            last_index = end

        # Any remaining text after the last link
        if last_index < len(text):
            remaining = text[last_index:]
            if remaining:
                new_nodes.append(TextNode(remaining, TextType.PLAIN))

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

            # INSERT_YOUR_CODE


def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        match = re.match(r"^#\s+(.+)", line.strip())
        if match:
            return match.group(1).strip()
    return None
