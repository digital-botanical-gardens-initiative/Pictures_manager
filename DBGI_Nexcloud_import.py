#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import requests

#Loads environment variables
load_dotenv()

#Access the environment variables
nextcloud_url = os.getenv('Instance_nextcloud')
username = os.getenv('next_user')
password = os.getenv('next_pass')
local_folder_path = os.getenv('out_jpg_path')

# Recursive function to create folder structure on Nextcloud
def create_folder_structure(folder_path, parent_folder_id):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            # Create a folder on Nextcloud
            response = requests.post(
                f"{nextcloud_url}/ocs/v1.php/apps/files_sharing/api/v1/shares",
                auth=(username, password),
                data={
                    'path': item,
                    'shareType': 3,
                    'permissions': 31,
                    'parent': parent_folder_id
                }
            )
            if response.status_code == 200:
                folder_id = response.json()['ocs']['data']['id']
                # Recursively create subfolders
                create_folder_structure(item_path, folder_id)
        else:
            print(f"Ignoring file: {item_path}")

# Upload files to Nextcloud
def upload_files(folder_path, parent_folder_id):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            # Upload file to Nextcloud
            with open(item_path, 'rb') as file:
                response = requests.put(
                    f"{nextcloud_url}/remote.php/dav/files/{username}/{parent_folder_id}/{item}",
                    auth=(username, password),
                    data=file
                )
                if response.status_code != 201:
                    print(f"Failed to upload file: {item_path}")
        else:
            print(f"Ignoring directory: {item_path}")

# Delete local files and folders
def delete_local_copies(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            # Recursively delete subfolders
            delete_local_copies(item_path)
            os.rmdir(item_path)
        else:
            os.remove(item_path)

# Main script
def main():
    # Create the root folder on Nextcloud
    response = requests.post(
        f"{nextcloud_url}/ocs/v1.php/apps/files_sharing/api/v1/shares",
        auth=(username, password),
        data={
            'path': os.path.basename(local_folder_path),
            'shareType': 3,
            'permissions': 31
        }
    )
    if response.status_code != 200:
        print("Failed to create root folder on Nextcloud")
        return

    root_folder_id = response.json()['ocs']['data']['id']

    # Create the folder structure on Nextcloud
    create_folder_structure(local_folder_path, root_folder_id)

    # Upload files to Nextcloud
    upload_files(local_folder_path, root_folder_id)

    # Delete local files and folders
    delete_local_copies(local_folder_path)

if __name__ == '__main__':
    main()
