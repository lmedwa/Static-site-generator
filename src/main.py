from copystatic import copy_static_recursive 
from gencontent import generate_page, generate_pages_recursive
import os 
import shutil


dir_path_static = "./static"
dir_path_public = "./public"
from_path = "./content/index.md"
temp_path = "./template.html"
dest_path = "./public/index.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    os.mkdir(dir_path_public)
    print("Copying static files to public directory")
    copy_static_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive("./content", "template.html", "./public")
main()