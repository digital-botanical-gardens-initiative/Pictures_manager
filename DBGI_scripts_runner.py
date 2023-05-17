#!/usr/bin/env python3

import subprocess
from dotenv import load_dotenv

#Loads environment variables
load_dotenv()

#Access the environment variables
script_inat = os.getenv('inat_script')

# Run script 1
subprocess.run(['python3', './DBGI_files_downloader.py']).check_returncode()

# Rerun script 1 in case of downloads errors
subprocess.run(['python3', './DBGI_files_downloader.py']).check_returncode()

# Run script 2
subprocess.run(['python3', './DBGI_CSV_creator.py']).check_returncode()

# Run script 3
subprocess.run(['python3', './DBGI_CSV_preparator.py']).check_returncode()

# Run script 4
subprocess.run(['python3', './DBGI_pictures_renamer.py']).check_returncode()

# Run script 5
subprocess.run(['python3', './DBGI_pictures_size_control.py']).check_returncode()

# Run script 6
subprocess.run(['python3', './DBGI_pictures_metadata_editor.py']).check_returncode()

# Run script 7
subprocess.run(['python3', './DBGI_inat_formatter.py']).check_returncode()

# Run script 8
subprocess.run(['python3', './DBGI_Nexcloud_import.py']).check_returncode()

#Run script 9
subprocess.run(['python3', script_inat]).check_returncode()


