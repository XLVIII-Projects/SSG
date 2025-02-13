from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from split_delimiter import split_nodes_delimiter

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)

    # delimit_node = split_nodes_delimiter(["This is a **text** node", TextType.BOLD])
    # print(delimit_node)


if __name__ == "__main__":
    main()