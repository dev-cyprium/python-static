from blocks import BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from utils import markdown_to_blocks, text_node_to_html_node, text_to_textnodes


def markdown_to_html_node(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html = block_type_to_html(block_type, block)

        if html:
            children.append(html)

    return ParentNode("div", children)


def block_type_to_html(block_type, block):
    match block_type:
        case BlockType.HEADING:
            return heading_to_html(block)
        case BlockType.PARAGRAPH:
            return parag_to_html(block)
        case _:
            return None


def parag_to_html(block):
    normalized = block.replace("\n", " ")
    text_nodes = text_to_textnodes(normalized)
    children = []

    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    return ParentNode("p", children)


def heading_to_html(block):
    h_level = block.count("#")
    value = block.replace("#", "").strip()
    return LeafNode(
        f"h{h_level}",
        value,
    )
