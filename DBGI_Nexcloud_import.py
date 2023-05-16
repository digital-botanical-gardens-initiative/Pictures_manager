#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import shutil

#Loads environment variables
load_dotenv()

#Access the environment variables
local_path = os.getenv('out_jpg_path')
remote_pic_path = os.getenv('nextcloud_path_pic')
remote_csv_path = os.getenv('nextcloud_path_pic')

# Iterate over the directory tree rooted at the input folder
for root, dirs, files in os.walk(local_path):
    # Create the corresponding output directory structure
    rel_path = os.path.relpath(root, local_path)
    output_dir = os.path.join(remote_pic_path, rel_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Move files from the input directory to the corresponding output directory
    for file in files:
        input_file = os.path.join(root, file)
        output_file = os.path.join(output_dir, file)
        shutil.move(input_file, output_file)

print("Files moved successfully.")
