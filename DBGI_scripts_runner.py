#!/usr/bin/env python3

import subprocess

# Run script 1
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
#subprocess.run(['python', './']).check_returncode()

