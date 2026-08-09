from textnode import TextNode, TextType
from enum import Enum
from textnode import text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdwon import text_to_textnodes


class MarkdownBlock(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"



def markdown_to_blocks(markdown: str) -> list[str]:
    block_strings = []
    sep_blocks = markdown.split("\n\n")
    for block in sep_blocks:
        bare_block = block.strip()
        if len(bare_block) > 0:
            block_strings.append(bare_block)

    return block_strings

def block_to_block_type(bare_block):
    if len(bare_block) > 0:
        lines = bare_block.split("\n")

        if bare_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return MarkdownBlock.heading

        if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
            return MarkdownBlock.code

        if bare_block.startswith(">"):
            for line in lines:
                if not line.startswith(">"):
                    return MarkdownBlock.paragraph
            return MarkdownBlock.quote

        if bare_block.startswith("- "):
            for line in lines:
                if not line.startswith("- "):
                    return MarkdownBlock.paragraph
            return MarkdownBlock.unordered_list

        i = 1
        if bare_block.startswith(f"{i}. "):
            for line in lines:
                if not line.startswith(f"{i}. "):
                    return MarkdownBlock.paragraph
                i += 1
            return MarkdownBlock.ordered_list
            

    return MarkdownBlock.paragraph

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    results = []
    for node in text_nodes:
        convert_item = text_node_to_html_node(node)
        results.append(convert_item) 
    return results   

def markdown_to_html_node(markdown):
    block_node_list = []
    split_blocks = markdown_to_blocks(markdown)
    for block in split_blocks:
        block_type = block_to_block_type(block)

        if block_type == MarkdownBlock.heading:
            level = 0 
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break 
            tag = f"h{level}"
            heading_text = block[level + 1:]
            children = text_to_children(heading_text)
            block_node_list.append(ParentNode(tag, children, None))

        if block_type == MarkdownBlock.code:
            code_text = block[3:-3]
            code_text = code_text[1:]
            code_text_node = TextNode(code_text, TextType.TEXT)
            code_leaf_node = text_node_to_html_node(code_text_node)
            code_node = ParentNode("code", [code_leaf_node])
            pre_node = ParentNode("pre", [code_node])
            block_node_list.append(pre_node)

        if block_type == MarkdownBlock.quote:
            clean_lines = []
            lines = block.split("\n")
            for line in lines:
                clean_line = line[1:].strip()
                clean_lines.append(clean_line)
            quote_text = " ".join(clean_lines)
            children = text_to_children(quote_text)
            block_node_list.append(ParentNode("blockquote", children, None))

        if block_type == MarkdownBlock.unordered_list:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                code_text = line[2:]
                children = text_to_children(code_text)
                li_nodes.append(ParentNode("li", children, None))
            block_node_list.append(ParentNode("ul", li_nodes, None))

        if block_type == MarkdownBlock.ordered_list:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                parts = line.split(". ", 1)
                item_text = parts[1]   
                children = text_to_children(item_text)
                li_nodes.append(ParentNode("li", children, None))
            block_node_list.append(ParentNode("ol", li_nodes, None))

        if block_type == MarkdownBlock.paragraph:
            lines = block.split("\n")
            paragraph_text = " ".join(lines)
            children = text_to_children(paragraph_text)
            block_node_list.append(ParentNode("p", children, None))

    return ParentNode("div", block_node_list, None)
            