from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.splitlines()
    non_empty_lines = [line for line in lines if line.strip() != ""]

    for line in lines:
        l = line.lstrip()
        if l != "":
            if re.match(r"^#{1,6} ", l):
                return BlockType.HEADING
            break

    stripped = block.strip()
    if stripped.startswith("```") and stripped.endswith("```"):
        code_lines = stripped.splitlines()
        if (
            len(code_lines) >= 2
            and code_lines[0].startswith("```")
            and code_lines[-1].startswith("```")
        ):
            return BlockType.CODE

    if len(non_empty_lines) > 0:

        if all(line.lstrip().startswith(">") for line in non_empty_lines):
            return BlockType.QUOTE

    if len(non_empty_lines) > 0 and all(
        re.match(r"^- ", line.lstrip()) for line in non_empty_lines
    ):
        return BlockType.UNORDERED_LIST

    if len(non_empty_lines) > 0:
        ordered = True
        for idx, line in enumerate(non_empty_lines, start=1):
            if not re.match(rf"^{idx}\. ", line.lstrip()):
                ordered = False
                break
        if ordered and re.match(r"^1\. ", non_empty_lines[0].lstrip()):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
