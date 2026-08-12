import os
import shutil


def copy_static_recursive(source_dir_path, dest_dir_path):
    for filename in os.listdir(source_dir_path):

        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            print(f"FILE: {from_path} -> {dest_path}")
            shutil.copy(from_path, dest_path)
        else:
            print(f"DIR: {from_path} -> {dest_path}")
            os.mkdir(dest_path)
            copy_static_recursive(from_path, dest_path)

        
