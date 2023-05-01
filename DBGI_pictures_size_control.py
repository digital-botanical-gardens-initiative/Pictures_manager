#!/usr/bin/env python3

from dotenv import load_dotenv
from PIL import Image
import os

#Loads environment variables
load_dotenv()

#Access the environment variables
in_jpg_path = os.getenv('in_jpg_path')

def compress_image(filepath):
    max_size = 5000000 # 5MB
    img = Image.open(filepath)
    if os.path.getsize(filepath) <= max_size:
        print(f"{filepath} is already small enough.")
        return
    else:
        print(f"Compressing {filepath}...")
        img.save(filepath, optimize=True, quality=80)
        while os.path.getsize(filepath) > max_size:
            img.save(filepath, optimize=True, quality=img.info['quality']-5)
        print(f"{filepath} compressed successfully.")

input_folder = in_jpg_path

for root, dirs, files in os.walk(input_folder):
    for filename in files:
        if filename.endswith('.jpg'):
            filepath = os.path.join(root, filename)
            compress_image(filepath)

