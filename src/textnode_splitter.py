from textnode import TextNode, TextType
from markdown_parser import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) == 1:
            new_nodes.append(node)
            continue
        if len(split_text) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(split_text)):
            if split_text[i]:
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        img_tuple = extract_markdown_images(node.text)
        if not img_tuple:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for img in img_tuple:
            split_nodes = remaining_text.split(f"![{img[0]}]({img[1]})")
            # print(f"print split nodes: {split_nodes}")
            if split_nodes[0]:
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT)) 
            if img[0] and img[1]:
                new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
            remaining_text = split_nodes[1]
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_tuple = extract_markdown_links(node.text)
        if not link_tuple:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for link in link_tuple:
            split_nodes = remaining_text.split(f"[{link[0]}]({link[1]})")
            if split_nodes[0]:
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
            if link[0] and link[1]:
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            remaining_text = split_nodes[1]
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes


            
