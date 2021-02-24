import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib
import download_from_id_song
import json

# Loading config variables
with open('config.json') as f:
    config = json.load(f)

# Loading "stop words" list. Songs that contain any of the "stop words" (remix, etc...) won't be downloaded
stop_words = config['stop_words']

# Loading output path where .pcm will be stored
output_path = config['output_path']


def main():
    print('# This script will download all .wav files from a game in smashcustommusic.net and convert them to .pcm files #\n')

    # If the script was runned directly without parameters
    if len(sys.argv) < 3:
        id_game = int(input('> Enter Game ID:\n'))
        folder_end = input('> Enter Name of output folder (default: output):\n').replace(' ', '_')
        if folder_end == "":
            print("Using default folder: output")
            folder_end = "output"
            
    # If the script was runned directly with parameters sent by the command line interface
    else:
        id_game = int(sys.argv[1])
        folder_end = sys.argv[2]

    url = "https://smashcustommusic.net/game/"
    req = requests.get(url + str(id_game), download_from_id_song.headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    
    game = soup.find_all("h1")

    # Get all links from game webpage
    rows = soup.find_all("a", href=True)
    # Filter links to keep only game songs that do not contain a "stop word" 
    data = {row.text: row['href'] for row in rows if 'song' in row['href'] and not any([word in row.text.lower() for word in stop_words])}

    print("Downloading songs from:", game[0].text, "- Total number of songs:", len(data) )

    # For each song to download, we call the script download_from_id_song to download, convert and save it
    for i, song_name in enumerate(data):
        song_id = data[song_name].split('/')[-1]

        try:
            # Sending parameters to function that will download song. stop_if_exists is True to ensure we don't download a song twice
            return_code = download_from_id_song.smash_wav_to_pcm(song_id, folder_end, verbose=False, stop_if_exists=True)
            
            # Song has been successfully downloaded
            if return_code == 1:
                print("Downloaded", song_name, "- Progress:", i+1, '/', len(data) )
            # Song was skipped because already downloaded
            else:
                print("Skipped", song_name, "- Progress:", i+1, '/', len(data) )
            
        except Exception as e:
            print("ID:", song_id, "Name:", song_name, "Error:", e)
            
    input("Process complete! .pcm available in folder '{}'. Press enter to finish.\n".format(output_path + folder_end))
    
if __name__ == "__main__":
    main()