from textnode import TextNode, TextType
import unittest
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        
        sections = node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise Exception(f"Unmatched delimiter '{delimiter}' in text: {node.text}")

        split_nodes = []

        for i, section in enumerate(sections):
            if i % 2 == 0:
                split_nodes.append(TextNode(section, TextType.TEXT))
            else:
                split_nodes.append(TextNode(section, text_type))

        new_nodes.extend(split_nodes)
    return new_nodes
        
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r'!\[([^\[\]]+)\]\(([^\(\)]+)\)', text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r'(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)', text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt_text, url in images:
            sections = remaining_text.split(f"![{alt_text}]({url})")
            before = sections[0]
            remaining_text = sections[1]
            if len(before) > 0:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE,url))

        if len(remaining_text) > 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for text, url in links:
            sections = remaining_text.split(f"[{text}]({url})")
            before = sections[0]
            remaining_text = sections[1]
            if len(before) > 0:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))

        if len(remaining_text) > 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def test_plain_text(self):
    new_nodes = text_to_textnodes("This is ")
    self.assertListEqual(
        [TextNode("This is ", TextType.TEXT)],
        new_nodes,
    )



def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is text with a link [to boot dev](https://www.boot.dev)"
    )
    self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ],
        new_nodes,
    )

def test_no_images(self):
    node = TextNode(
        "This is text with an and another",
        TextType.TEXT
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [node],
        new_nodes,
    )

def test_image_at_start(self):
    node = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png) This is text with an and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("This is text with an and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ],
        new_nodes,
    )