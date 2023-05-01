#!/usr/bin/env python3

from PIL import Image
import os


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

input_folder = '/home/dbgi/input/pictures'

for root, dirs, files in os.walk(input_folder):
    for filename in files:
        if filename.endswith('.jpg'):
            filepath = os.path.join(root, filename)
            compress_image(filepath)

