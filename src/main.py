from textnode import TextNode
from textnode import TextType

def main():
    node = TextNode("This is a text node", TextType.bold_text, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()