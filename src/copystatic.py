import os
import shutil

def copy_files_recursive(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    entries = os.listdir(source)
    for entry in entries:
        src_path = os.path.join(source, entry)
        dst_path = os.path.join(destination, entry)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_files_recursive(src_path, dst_path)