#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import shutil

#Loads environment variables
load_dotenv()

#Access the environment variables
local_path = os.getenv('out_path')
remote_path = os.getenv('nextcloud_path')
nextcloud_data_folder = os.getenv('next_folder_path')

def upload_files_recursive(local_path, remote_path):
    for item in os.listdir(local_path):
        item_path = os.path.join(local_path, item)
        remote_item_path = os.path.join(remote_path, item)

        if os.path.isfile(item_path):
            # Move file to Nextcloud data folder and overwrite if it already exists
            remote_file_path = os.path.join(nextcloud_data_folder, remote_item_path[len(local_path) + 1:])
            remote_file_dir = os.path.dirname(remote_file_path)
            os.makedirs(remote_file_dir, exist_ok=True)
            shutil.move(item_path, remote_file_path)
            print(f"Moved file: {item_path} -> {remote_file_path}")
        elif os.path.isdir(item_path):
            # Check if directory exists in Nextcloud data folder
            remote_directory_path = os.path.join(nextcloud_data_folder, remote_item_path[len(local_path) + 1:])
            if not os.path.exists(remote_directory_path):
                # Create directory in Nextcloud data folder if it doesn't exist
                os.makedirs(remote_directory_path)
                print(f"Created remote directory: {remote_item_path}")

            # Recursively move files within the directory
            upload_files_recursive(item_path, remote_item_path)

upload_files_recursive(local_path=local_path, remote_path=remote_path)
