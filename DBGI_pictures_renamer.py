#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import re

#Loads environment variables
load_dotenv()

#Access the environment variables
in_jpg_path = os.getenv('in_jpg_path')

root_folder = in_jpg_path

for root, dirs, files in os.walk(root_folder):
    for filename in files:
        # split the filename into base and extension
        base, ext = os.path.splitext(filename)
        # replace spaces with underscores in the base filename
        base = base.replace(" ", "_")
        # remove non-alphanumeric characters from base filename
        base = re.sub(r"[^\w\s]", "", base)
        # join the modified base filename and original extension
        new_filename = base + ext
        # rename file
        os.rename(os.path.join(root, filename), os.path.join(root, new_filename))
