from markdown_blocks import markdown_to_html_node
import os
from pathlib import Path

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
        else:
            raise Exception("No title found in the markdown content.")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        from_contents = f.read()

    with open(template_path) as f:
        temp_contents = f.read()

    resulting_node = markdown_to_html_node(from_contents)
    HTML_string = resulting_node.to_html()

    page_title = extract_title(from_contents)

    resulting_page = temp_contents.replace("{{ Title }}", page_title).replace("{{ Content }}", HTML_string)
    resulting_page = resulting_page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    dest_path_directory = os.path.dirname(dest_path)
    os.makedirs(dest_path_directory, exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(resulting_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    entry_names = os.listdir(dir_path_content)

    for entry in entry_names:
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)