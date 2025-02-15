#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
PYTHONPATH=src python3 -m unittest discover -s src


# python3 -m unittest src.test_inline_markdown.TestSplitNode.test_split_boldnode
# python3 -m unittest src.test_inline_markdown.TestMarkdownImg.test_inline_img
# python3 -m unittest src.test_inline_markdown.MarkdownToHTMLNode.test_markdown_to_html_node_text1
# 