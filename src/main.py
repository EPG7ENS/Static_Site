import os
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def generate_pages_recursive(dir_path_content, template_path, dir_path_public):
    for entry in os.listdir(dir_path_content):
        content_entry_path = os.path.join(dir_path_content, entry)
        public_entry_path = os.path.join(dir_path_public, entry)
        if os.path.isfile(content_entry_path):
            
            if content_entry_path.endswith(".md"):
                output_html_path = public_entry_path.replace(".md", ".html")

                generate_page(
                    content_entry_path,   # the markdown file
                    template_path,        # the template
                    output_html_path,     # where to write HTML
                )
            
        else:
            os.makedirs(public_entry_path, exist_ok=True)

            # now recurse into that folder
            generate_pages_recursive(
                content_entry_path,  # new content dir
                template_path,       # same template
                public_entry_path,   # matching public dir
            )
        
        
def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_pages_recursive(dir_path_content,template_path,dir_path_public)
    


main()