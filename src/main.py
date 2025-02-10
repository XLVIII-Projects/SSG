from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    node = TextNode("This is a text node", TextType.bold_text, "https://www.boot.dev")
    print(node)



if __name__ == "__main__":
    main()