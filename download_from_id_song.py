import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib
import generate_pcm_from_wav

output_path = generate_pcm_from_wav.output_path

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    
url = "https://smashcustommusic.net/song/"


def download_song(song_id, song_file):
    """
    Download a song from smash website using its id
    
    :song_id: id of song in smash website
    :song_file: name of song file after download
    :return: path to output song
    """
    
    URL_down = "https://smashcustommusic.net/wav/" + str(song_id)

    current_path = generate_pcm_from_wav.current_path
    folder_in = generate_pcm_from_wav.folder_in
    
    path_out = current_path + folder_in + '/' + song_file

    urllib.request.urlretrieve(URL_down, path_out)
    
    return path_out
    
    
def get_metadata(id_song):
    """
    Get song metadata (such as looping points and sampling rate) using song id
    
    :song_id: id of song in smash website    
    :return: song metadata as dict
    """
    
    url = "https://smashcustommusic.net/song/" + str(id_song)
    req = requests.get(url , headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    rows = soup.find_all("tr")
    data = {}
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols)==2:
            # Get rid of empty values
            data[cols[0]]= cols[1]
            
    return data


def main():
    print('# This script will download a .wav file from smashcustommusic.net and convert it to a .pcm file #\n')

    # If the script was runned directly without parameters
    if len(sys.argv) < 3:
        id_song = int(input('> Enter Song ID:\n'))
        folder_end = input('> Enter Name of output folder (default: output):\n').replace(' ', '_')
        if folder_end == "":
            print("Using default folder: output")
            folder_end = "output"
            
    # If the script was runned directly with parameters sent by the command line interface
    else:
        id_song = int(sys.argv[1])
        folder_end = sys.argv[2]
        
    smash_wav_to_pcm(id_song, folder_end)
    
    input("Process complete! .pcm available in folder '{}'. Press enter to finish.\n".format(output_path + folder_end))

    
def smash_wav_to_pcm(id_song, folder_end, verbose=True, stop_if_exists=False):
    """
    Convert input .wav to a valid 16-bit 44.1 KHz .wav
    Then, from this valid .wav generate a .pcm and normalize it
    Finally the normalized .pcm is saved in output folder
    
    :id_song: id of song in smash website
    :folder_end: name of output folder
    :verbose: True if we print info. Should be False if called from another script
    :stop_if_exists: True if we want to stop process if song already downloaded
    :return: 0 if song was skipped because it already exists. 1 otherwise 
    """

    data = get_metadata(id_song)
            
    sample_rate = data['Sampling Rate:']
    start_loop = data['Start Loop Point:']
    name_song = data['Song Name:'].replace(' ', '_').replace(':', '').replace('/', '').replace('/', '')

    if verbose:
        print("Downloading", name_song)

    song_file = "{}.wav".format(name_song)
    
    # Path to output folder
    path_final = generate_pcm_from_wav.output_path + folder_end + '/'
    # Path to output .pcm
    path_final_normalized = path_final + folder_end + '-' + name_song + '.pcm'
    # If .pcm already exist and stop_if_exists is True, we stop the process
    if stop_if_exists and os.path.exists(path_final_normalized):
        return 0

    path_out = download_song(id_song, song_file)

    # Convert downloaded .wav to normalized .pcm
    generate_pcm_from_wav.wav_to_normalized_pcm(folder_end, song_file, sample_rate, start_loop)
    
    return 1

    
if __name__ == "__main__":
    main()