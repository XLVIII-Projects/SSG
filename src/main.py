import os
import shutil

from markdown_to_html_node import markdown_to_html_node

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.makedirs("public")

    # copy static files
    copy_source_to_dest("static", "public")

    # generate html page
    generate_pages_recursive("content", "template.html", "public")

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("Error: no heading found starting with '# '")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    directory_items = os.listdir(dir_path_content)
    for item in directory_items:
        source_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item).replace(".md",".html")
        # dest_path = dest_path.replace(".md",".html")
        if os.path.isdir(source_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(source_path, template_path, dest_path)
        elif source_path.endswith(".md"):
            generate_page(source_path, template_path, dest_path)
        else:
            continue

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()
       
    markdown_html_node = markdown_to_html_node(markdown_content)
    markdown_html_string = markdown_html_node.to_html()
    title = extract_title(markdown_content)
    
    with open(template_path, "r") as template_file:
        template_content = template_file.read()
    
    final_content = template_content.replace("{{ Title }}", title)
    final_content = template_content.replace("{{ Content }}", markdown_html_string)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(final_content)

def copy_source_to_dest(source, dest):
    directory_items = os.listdir(source)
    for item in directory_items:
        source_path = os.path.join(source, item)
        dest_path = os.path.join(dest, item)
        if os.path.isdir(source_path):
            os.makedirs(dest_path, exist_ok=True)
            copy_source_to_dest(source_path, dest_path)
        else:
            shutil.copy(source_path, dest_path)

if __name__ == "__main__":
    main()