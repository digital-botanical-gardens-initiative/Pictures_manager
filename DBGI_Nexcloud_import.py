#!/usr/bin/env python3

from dotenv import load_dotenv
import os
from nextcloud import NextCloud

#Loads environment variables
load_dotenv()

#Access the environment variables
nextcloud_url = os.getenv('Instance_nextcloud')
username = os.getenv('next_user')
password = os.getenv('next_pass')
login_endpoint = nextcloud_url + "/ocs/v1.php/cloud/user?format=json"
local_folder_path = os.getenv('out_jpg_path')

nxc = NextCloud(endpoint=nextcloud_url, user=username, password=password)

nxc.get_users()