import os
import subprocess
from pathlib import Path

"""
# Prompt the user for the SoundCloud playlist URL and folder name
playlist_url = input("Enter the SoundCloud playlist URL: ")
playlist_name = input("Enter new folder name: ")

# Set the Downloads folder path
downloads_folder = Path.home() / "Downloads"

# Create a folder with the playlist title within the Downloads folder
playlist_folder = downloads_folder / playlist_name

if not os.path.exists(playlist_folder):
    os.makedirs(playlist_folder)

# Change the current working directory to the new folder
os.chdir(playlist_folder)

# Use youtube-dl to download the playlist as WAV files
subprocess.run(["youtube-dl", "--no-check-certificate", "-i", "--extract-audio", "--audio-format", "wav", "-o",
                "%(title)s.%(ext)s", playlist_url])

print(f"Playlist downloaded and saved as WAV files in {playlist_folder} directory")

# Open the directory when done
subprocess.run(["open", playlist_folder])
"""

import os
import subprocess
from pathlib import Path

# Prompt the user for the SoundCloud playlist URL and folder name
playlist_url = input("Enter the SoundCloud playlist URL: ")
playlist_name = input("Enter new folder name: ")

# Get the user's home directory
home_directory = os.path.expanduser("~")

# Set the Downloads folder path
downloads_folder = Path(home_directory) / "Downloads"

# Create a folder with the playlist title within the Downloads folder
playlist_folder = downloads_folder / playlist_name

if not os.path.exists(playlist_folder):
    os.makedirs(playlist_folder)

# Change the current working directory to the new folder
os.chdir(playlist_folder)

# Use youtube-dl to download the playlist as WAV files
subprocess.run(["youtube-dl", "--no-check-certificate", "-i", "--extract-audio", "--audio-format", "wav", "-o",
                "%(title)s.%(ext)s", playlist_url])

print(f"Playlist downloaded and saved as WAV files in {playlist_folder} directory")

# Open the directory when done
subprocess.run(["open", playlist_folder])
