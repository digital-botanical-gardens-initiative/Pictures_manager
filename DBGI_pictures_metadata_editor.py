#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import subprocess
import csv
import re

#Loads environment variables
load_dotenv()

#Access the environment variables
in_jpg_path = os.getenv('in_jpg_path')
out_csv_path = os.getenv('out_csv_path')
out_jpg_path = os.getenv('out_jpg_path')

# Define paths
pictures_folder = in_jpg_path
csv_folder = out_csv_path
output_folder = out_jpg_path

# Loop over pictures
for root, dirs, files in os.walk(pictures_folder):
    for file in files:
        if file.lower().endswith('.jpg'):
            picture_path = os.path.join(root, file)

            # Get unique identifier from picture name
            unique_id = re.search(r"dbgi_[0-9]+", file).group()
            unique_prefixed = 'emi_external_id:' + unique_id

            # Get corresponding CSV file
            csv_filename = os.path.join(csv_folder, os.path.basename(os.path.dirname(root)), os.path.basename(root) + '_EPSG:4326.csv')

            # Check if CSV file exists
            if not os.path.isfile(csv_filename):
                print(f"No corresponding CSV file found for {picture_path}")
                continue

            # Get coordinates from CSV file
            with open(csv_filename, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['spl_code'] == unique_id:
                        lon = row['latitude']
                        lat = row['longitude']
                        break
                else:
                     print(f"No coordinates found for {unique_id} in {csv_filename}")
                     continue

            # Define output filename with unique identifier
            # Get relative path to input file
            relative_path = os.path.relpath(picture_path, pictures_folder)

            # Define output path based on relative path
            output_path = os.path.join(output_folder, relative_path)

            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write metadata using exiftool
            command = f"exiftool -Subject={unique_prefixed} -GPSLongitudeRef=East -XMP:GPSLongitude={lon} -GPSLatitudeRef=North -XMP:GPSLatitude={lat} {picture_path} -overwrite_original -o {output_path}"
            subprocess.run(command, shell=True)

            print(f"Metadata written for {picture_path}")
