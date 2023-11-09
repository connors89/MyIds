import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import concurrent.futures
import os
import yt_dlp
import ffmpeg
import concurrent.futures
import subprocess
import sys


# -------------------------------------------------------------

import os
from pathlib import Path
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import concurrent.futures
import yt_dlp
import ffmpeg
import concurrent.futures


# ---------------------------------------------------------------
def spoti():
    # Function to write songs to text file
    def write_tracks(download_dir):  # Pass the download directory as an argument
        # playlist_file = open(playlist_name)
        with open(playlist_name, 'a', encoding='utf-8') as file:
            for track in playlist['items']:
                track_name = track['track']['name']
                artists = ", ".join([artist['name'] for artist in track['track']['artists']])
                file.write(f"{track_name} - {artists}\n")
        print(f'Success! The playlist tracks have been written to', playlist_name)

        os.makedirs(download_dir, exist_ok=True)  # Create the download directory if it doesn't exist


    # Function to download a single YouTube video
    def download_youtube_video(query, output_path):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path + '.webm',
            'default_search': 'ytsearch',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])


    # Function to convert .webm to .mp3 using ffmpeg-python
    def convert_to_mp3(input_path, output_path):
        input_stream = ffmpeg.input(input_path)
        output_stream = ffmpeg.output(input_stream, output_path + '.mp3')
        ffmpeg.run(output_stream)


    def convert_to_wav(input_path, output_path):
        input_stream = ffmpeg.input(input_path)
        output_stream = ffmpeg.output(input_stream, output_path + '.wav')
        ffmpeg.run(output_stream)


    # Function to remove .webm files
    def remove_webm_files(folder):
        for filename in os.listdir(folder):
            if filename.endswith('.webm') or \
                    filename.endswith('.webm.ytdl') or \
                    filename.endswith('.webm.part') or \
                    filename.endswith('.txt'):
                os.remove(os.path.join(folder, filename))

                # Function to process a list of songs from a .txt file

    def process_songs_WAV(txt_file, download_dir):  # Pass the download directory as an argument
        folder_name = os.path.splitext(txt_file)[0]

        with open(txt_file, 'r') as file:
            queries = [f'{line.strip()} audio' for line in file]

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for query in queries:
                title_artist = query.split(' audio')[0]
                output_path = os.path.join(download_dir, f'{title_artist}')  # Use download_dir here
                executor.submit(download_youtube_video, query, output_path)

        # Wait for all downloads to finish before proceeding
        executor.shutdown()

        # Convert .webm to .mp3 in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as converter_executor:
            for query in queries:
                title_artist = query.split(' audio')[0]
                input_path = os.path.join(download_dir, f'{title_artist}.webm')  # Use download_dir here
                output_path = os.path.join(download_dir, f'{title_artist}')  # Use download_dir here
                converter_executor.submit(convert_to_wav, input_path, output_path)
        # Remove .webm files after conversion
        remove_webm_files(download_dir)  # Use download_dir here


    if __name__ == "__main__":
        print("Welcome to the Spotify to MP3/WAV downloader!")
        # txt_file = 'spd26.txt'  # Replace with the name of your .txt file
        # Set your Spotify API credentials
        client_id = 'd8e2f4c34bea469c9285e7a706cc1d5c'
        client_secret = '47a56195e3394028aa0e629125815a66'
        # Initialize the Spotify API client with the Client Credentials Flow
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
        # Specify the Spotify playlist URI (you don't need user-specific playlists for this flow)
        playlist_uri = input("\nEnter Spotify playlist URL: ")
        #MP3_or_WAV = input("\nPress 1 for MP3\nPress 2 for WAV: ")
        # Retrieve the playlist and its tracks
        playlist = sp.playlist_tracks(playlist_uri)
        # Extract and write the track names to a text file
        txt = ".txt"
        Pname = input("Enter name for playlist: ")
        playlist_name = Pname + txt

        # Get the user's "Downloads" folder
        downloads_folder = os.path.expanduser("~/Downloads")
        download_dir = os.path.join(downloads_folder, playlist_name.replace(".txt", ""))

        write_tracks(download_dir)  # Pass the download directory as an argument
        process_songs_WAV(playlist_name, download_dir)
        print(f"Downloads are complete! You can find your files in the folder: {download_dir}")

        # Open the directory using the default file manager
        subprocess.run(["open", download_dir])



spoti()

# -------------------------------------------


