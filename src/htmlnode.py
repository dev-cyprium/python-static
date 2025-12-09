from multiprocessing import Value


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""

        arr = []
        for k, v in self.props.items():
            arr.append(f'{k}="{v}"')

        arr[0] = f" {arr[0]}"
        return " ".join(arr)

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required for ParentNode")

        if not self.children:
            raise ValueError("children are required for ParentNode")

        buffer = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            buffer += child.to_html()

        buffer += f"</{self.tag}>"
        return buffer


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError()

        if not self.tag:
            return str(self.value)

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
