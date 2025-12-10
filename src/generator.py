from blocks import BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from utils import markdown_to_blocks, text_node_to_html_node, text_to_textnodes
import re


def markdown_to_html_node(markdown) -> HTMLNode:
    """Convert full markdown string into an HTML node tree."""
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html = block_type_to_html(block_type, block)

        if html:
            children.append(html)

    return ParentNode("div", children)


def block_type_to_html(block_type, block):
    """Dispatch block rendering based on detected block type."""
    match block_type:
        case BlockType.HEADING:
            return heading_to_html(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_html(block)
        case BlockType.CODE:
            return codeblock_to_html(block)
        case BlockType.QUOTE:
            return quote_to_html(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html(block)
        case _:
            return None


def _inline_children_from_text(text):
    """Parse inline markdown inside a line and return HTML child nodes."""
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def paragraph_to_html(block):
    normalized = block.replace("\n", " ")
    children = _inline_children_from_text(normalized)
    return ParentNode("p", children)


def heading_to_html(block):
    """Render heading (# .. ######) into an h1-h6 node with inline children."""
    match = re.match(r"^(#{1,6})\s+(.*)", block.strip())
    if not match:
        # fallback to paragraph if the heading is malformed
        return paragraph_to_html(block)

    hashes, content = match.groups()
    children = _inline_children_from_text(content.strip())
    return ParentNode(f"h{len(hashes)}", children)


def codeblock_to_html(block):
    """Render fenced code block."""
    lines = block.splitlines()
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].startswith("```"):
        content_lines = lines[1:-1]
    else:
        content_lines = lines

    # Join with newline and preserve a trailing newline for readability / tests
    code_text = "\n".join(content_lines)
    if not code_text.endswith("\n"):
        code_text += "\n"

    code_node = LeafNode("code", code_text)
    return ParentNode("pre", [code_node])


def quote_to_html(block):
    lines = []
    for line in block.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(">"):
            lines.append(stripped[1:].lstrip())
        else:
            lines.append(stripped)

    text = " ".join(lines)
    children = _inline_children_from_text(text)
    return ParentNode("blockquote", [ParentNode("p", children)])


def _list_items_to_html(lines):
    """Convert a list of raw lines into <li> nodes with inline children."""
    items = []
    for line in lines:
        text = line.strip()
        items.append(ParentNode("li", _inline_children_from_text(text)))
    return items


def unordered_list_to_html(block):
    lines = block.splitlines()
    cleaned = [re.sub(r"^-+\s*", "", line.strip(), count=1) for line in lines]
    return ParentNode("ul", _list_items_to_html(cleaned))


def ordered_list_to_html(block):
    lines = block.splitlines()
    cleaned = [re.sub(r"^\d+\.\s*", "", line.strip(), count=1) for line in lines]
    return ParentNode("ol", _list_items_to_html(cleaned))
