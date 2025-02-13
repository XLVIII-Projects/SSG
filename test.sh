export PYTHONPATH=$(pwd)

python3 -m unittest discover -s src

# python3 -m unittest src.test_inline_markdown.TestSplitNode.test_split_boldnode
# python3 -m unittest src.test_inline_markdown.TestMarkdownImg.test_inline_img