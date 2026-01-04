import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def generate_pages_recursive(src_dir, template_path, dest_dir, basepath):
    os.makedirs(dest_dir, exist_ok=True)

    for item in os.listdir(src_dir):
        from_path = os.path.join(src_dir, item)

        if os.path.isdir(from_path):            
            generate_pages_recursive(
                from_path,
                template_path,
                os.path.join(dest_dir, item),
                basepath
            )
        elif from_path.endswith(".md"):
            stem = Path(item).stem

            if stem == "index":
                dest_path = os.path.join(dest_dir, "index.html")
            else:                
                page_dir = os.path.join(dest_dir, stem)
                os.makedirs(page_dir, exist_ok=True)
                dest_path = os.path.join(page_dir, "index.html")

            generate_page(from_path, template_path, dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")

    with open(from_path, "r") as from_file:
        markdown_content = from_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()
    
    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as to_file:
        to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
