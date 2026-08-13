from copystatic import copy_static_recursive 
from gencontent import generate_page, generate_pages_recursive
import os 
import shutil
import sys


dir_path_static = "./static"
dir_path_docs = "./docs"
from_path = "./content/index.md"
temp_path = "./template.html"
dest_path = "./public/index.html"


def main():
    print("Deleting public directory...")

    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    os.mkdir(dir_path_docs)

    print("Copying static files to public directory")

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print(f"using: {basepath}")

    copy_static_recursive(dir_path_static, dir_path_docs)

    generate_pages_recursive("./content", "template.html", "./docs", basepath)

    
main()