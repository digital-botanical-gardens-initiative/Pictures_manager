#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import shutil
import glob
import re

#Loads environment variables
load_dotenv()

#Access the environment variables
out_jpg_path = os.getenv('out_jpg_path')
out_jpg_path2 = os.getenv('out_jpg_path2')

# Define paths
output_folder = out_jpg_path
output_folder2 = out_jpg_path2

#Create the target folder if it doesn't exist
os.makedirs(output_folder2, exist_ok=True)

# Loop over the pictures in the source folder and its subfolders
for file_path in glob.glob(os.path.join(output_folder, '**/*.jpg'), recursive=True):
    # Extract the unique identifier from the picture name
    file_name = os.path.basename(file_path)
    unique_id = re.search(r"(dbgi|emi)_\d+", file_name)
    if unique_id:
        unique_id = unique_id.group()
    else:
        print(f"Unique identifier not found for {file_name}")
        continue

    # Create the subfolder for the unique identifier in the target folder
    unique_folder = os.path.join(output_folder2, unique_id)
    os.makedirs(unique_folder, exist_ok=True)

    # Copy the picture to the subfolder in the target folder
    target_path = os.path.join(unique_folder, file_name)
    shutil.copy2(file_path, target_path)

    print(f"Copied {file_path} to {target_path}")
