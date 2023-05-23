#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import shutil
import subprocess

#Loads environment variables
load_dotenv()

#Access the environment variables
local_path = os.getenv('out_jpg_path')
local_path_csv = os.getenv('out_csv_path')
remote_pic_path = os.getenv('next_folder_path_pic')
remote_csv_path = os.getenv('next_folder_path_csv')

# Iterate over the pictures directory
for root, dirs, files in os.walk(local_path):
    # Create the corresponding output directory structure on Nextcloud
    rel_path = os.path.relpath(root, local_path)
    output_dir = os.path.join(remote_pic_path, rel_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Move pictures from the input directory to the corresponding output directory
    for file in files:
        input_file = os.path.join(root, file)
        output_file = os.path.join(output_dir, file)
        shutil.move(input_file, output_file)

print("Files moved successfully.")

# Iterate over the csv directory
for root, dirs, files in os.walk(local_path_csv):
    # Create the corresponding output directory structure on Nextcloud
    rel_path = os.path.relpath(root, local_path_csv)
    output_dir = os.path.join(remote_csv_path, rel_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Move pictures from the input directory to the corresponding output directory
    for file in files:
        input_file = os.path.join(root, file)
        output_file = os.path.join(output_dir, file)
        shutil.move(input_file, output_file)

print("Files moved successfully.")

#Run the command to scan Nextcloud files, so that they are showed into Nextcloud
scan_path = '/var/www/nextcloud'
scan_command = 'sudo -u www-data php occ files:scan --all'
subprocess.run(scan_command, shell=True, cwd=scan_path)