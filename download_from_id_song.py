import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib
import json
import generate_pcm_from_wav
from lib.functions import system_command, get_folder_final_info

# Loading config variables
with open('config.json') as f:
    config = json.load(f)

# Loading parent output folder where .pcm will be stored
output_path = config['output_path']

# Loading tools folder where msupcm.exe and wav2msu.exe are stored
tools_folder = config['tools_folder']

current_path = os.getcwd().replace('\\', '/') + '/'
# Loading temp folder where downloaded .pcm will be stored
temp_folder = config['temp_folder']

# Loading folder for looping audio converter
looping_audio_converter_path = config['looping_audio_converter_path']

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    
url = "https://smashcustommusic.net/song/"


def download_song(song_id, name_song, path_folder, format='brstm'):
    """
    Download a song from smash website using its id
    
    :song_id: id of song in smash website
    :name_song: name of song
    :path_folder: path to downloaded file
    :return: name of output song
    """
    
    URL_down = "https://smashcustommusic.net/{}/{}".format(format, song_id)

    song_file = '{}.{}'.format(name_song, format)
    path_out = path_folder + song_file

    urllib.request.urlretrieve(URL_down, path_out)
    
    return song_file
    
    
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
    
 
def brstm_to_wav(path_in, path_out, remove_brstm=True):
    """
    Convert brstm to 16 bit wav
    
    :path_in: path to downloaded .brstm
    :path_out: path to output .wav
    """
    
    system_command(tools_folder + 'VGAudioCli.exe "{}" "{}" -f pcm16'.format(path_in, path_out))
    if remove_brstm:
        os.remove(path_in)


def main():
    print('# This script will download a .wav file from smashcustommusic.net and convert it to a .pcm file #\n')

    # If the script was runned directly without parameters
    if len(sys.argv) < 2:
        id_song = int(input('> Enter Song ID:\n'))
        folder_end = input('> Enter Name of output folder:\n').replace(' ', '_')
            
    # If the script was runned directly with parameters sent by the command line interface
    else:
        id_song = int(sys.argv[1])
        if len(sys.argv) > 2:
            folder_end = sys.argv[2]
        else:
            folder_end = ""
        
    smash_brstm_process(id_song, folder_end)
    
    input("Process complete! .pcm available in folder '{}'. Press enter to finish.\n".format(output_path + folder_end))

    
def smash_brstm_process(id_song, folder_end, verbose=True, stop_if_exists=False):
    """
    Download brstm from smashcustommusic
    Convert brstm to pcm if auto_convert_brstm_to_pcm_with_vgaudio_librosa is true
    
    :id_song: id of song in smash website
    :folder_end: name of output folder
    :verbose: True if we print info. Should be False if called from another script
    :stop_if_exists: True if we want to stop process if song already downloaded
    :return: 0 if song was skipped because it already exists. 1 otherwise 
    """

    data = get_metadata(id_song)
            
    # sample_rate = data['Sampling Rate:']
    start_loop = data['Start Loop Point:']
    # end_loop = data['End Loop Point:']
    name_song = data['Song Name:'].replace(' ', '_').replace(':', '').replace('/', '').replace('/', '')

    if verbose:
        print("Downloading", name_song)
        
    # Get path to output folder and prefix to output file
    path_folder_final, prefix_file_final =  get_folder_final_info(output_path, folder_end)
    
    # Path to downloaded song
    path_brstm_folder = current_path + temp_folder + '/'
    
    # Path to output .pcm
    path_file_final = path_folder_final + prefix_file_final + name_song + '.pcm'
    
    # If .pcm already exist and stop_if_exists is True, we stop the process
    if stop_if_exists and os.path.exists(path_file_final):
        return 0

    # Download .brstm song and retrieve name of brstm file (with extension)
    brstm_file = download_song(id_song, name_song, path_brstm_folder, format='brstm')
           
    wav_file = name_song + '.wav'
    # Convert brstm to .wav
    brstm_to_wav(path_brstm_folder + brstm_file, looping_audio_converter_path + wav_file)
    
    generate_pcm_from_wav.wav_to_normalized_pcm(folder_end, wav_file, start_loop)
          
    return 1
    

    
if __name__ == "__main__":
    main()