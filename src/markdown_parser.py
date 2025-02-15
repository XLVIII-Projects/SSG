import re

def extract_markdown_images(text):
    img_tuple = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    if img_tuple == []:
        return []
    return img_tuple

def extract_markdown_links(text):
    link_tuple = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    if link_tuple == []:
        return []
    return link_tuple