from block_to_block_type import block_to_block_type
from htmlnode import LeafNode, ParentNode
from textnode_splitter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def markdown_to_blocks(markdown):
    markdown_list = markdown.split("\n\n")
    blocks = []
    for block in markdown_list:
        block = block.strip()
        if not block:
            continue
        blocks.append(block)
    return blocks

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    # print(nodes)
    return nodes

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"alt": text_node.text, "src": text_node.url})
    else:
        raise ValueError("Invalid TextType")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    list_of_html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        # print(f"printing block type: {block_type}")
        if block_type == "quote":
            html_node = markdown_to_blocks_quote(block)
        elif block_type == "unordered_list":
            html_node = markdown_to_blocks_unordered_list(block)
        elif block_type == "ordered_list":
            html_node = markdown_to_blocks_ordered_list(block)
        elif block_type == "code":
            html_node = markdown_to_blocks_code(block)
        elif block_type == "heading":
            html_node = markdown_to_blocks_heading(block)
        elif block_type == "paragraph":
            html_node = markdown_to_blocks_paragraph(block)
        elif block_type == None:
            continue
        else:
            raise ValueError("Invalid block type")
        list_of_html_nodes.append(html_node)
    return ParentNode("div", list_of_html_nodes)       

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    # print(text_nodes)
    children = []
    for text_node in text_nodes:    
        children.append(text_node_to_html_node(text_node))
    # print(children)
    return children

def markdown_to_blocks_quote(block):
    lines = block.split("\n")
    lines = [line.lstrip().removeprefix("> ") for line in lines]
    return ParentNode("blockquote", text_to_children("\n".join(lines)))
    
def markdown_to_blocks_unordered_list(block):
    lines = block.split("\n")
    lines = [line.lstrip().removeprefix("* ").removeprefix("- ") for line in lines]
    children_list = []
    for line in lines:
        children = text_to_children(line)
        children_list.append(ParentNode("li", children))
    return ParentNode("ul", children_list)

def markdown_to_blocks_ordered_list(block):
    lines = block.split("\n")
    children_list = []
    for line in lines:
        split_line = line.lstrip().split(". ", 1)
        if split_line[0].isdigit():
            children = text_to_children(split_line[1])
        else:
            children = text_to_children(line)
        children_list.append(ParentNode("li", children))
    return ParentNode("ol", children_list)

def markdown_to_blocks_code(block):
    block = block.replace("```", "")
    children = text_to_children(block)
    return ParentNode("pre", [ParentNode("code", children)])

def markdown_to_blocks_heading(block):
    level = 0
    while block[level] == "#":
        level += 1
    if level > 6:
        raise ValueError("Heading level is too high")
    if level == 0:
        raise ValueError("Heading level is too low")
    if level >= len(block):
        raise ValueError("Heading level is too high")
    block = block[level + 1:]
    children = text_to_children(block)
    return ParentNode(f"h{level}", children)

def markdown_to_blocks_paragraph(block):
    children = text_to_children(block)
    return ParentNode("p", children)




# Quote blocks should be surrounded by a <blockquote> tag.
# Unordered list blocks should be surrounded by a <ul> tag, and each list item should be surrounded by a <li> tag.
# Ordered list blocks should be surrounded by a <ol> tag, and each list item should be surrounded by a <li> tag.
# Code blocks should be surrounded by a <code> tag nested inside a <pre> tag.
# Headings should be surrounded by a <h1> to <h6> tag, depending on the number of # characters.
# Paragraphs should be surrounded by a <p> tag.