def block_to_block_type(block):
# Each helper returns either the type string or None
    return (block_heading(block) or 
            block_code(block) or 
            block_quote(block) or 
            block_unordered_list(block) or 
            block_ordered_list(block) or 
            "paragraph")

def block_heading(block):
    if block.startswith("#") or block.startswith("##") or block.startswith("###") or block.startswith("####") or block.startswith("#####") or block.startswith("######"): #check if block is a heading
        return "heading"    
    
def block_code(block):
    if block.startswith("```") and block.endswith("```"): #check if block is a code block
        return "code"    

def block_quote(block):
    lines = block.split("\n") #check if block is a quote
    for line in lines:
        if not line.startswith(">"):
            return False
    return "quote"    

def block_unordered_list(block):
    lines = block.split("\n") #check if block is an unordered list
    for line in lines:
        if not line.startswith("* ") and not line.startswith("- "):
            return False
    return "unordered_list"

def block_ordered_list(block):
    lines = block.split("\n") #check if block is an ordered list
    index = 1
    for line in lines:
        expected = f"{index}."
        if not line.startswith(expected):
            return False
        index += 1
    return "ordered_list"
