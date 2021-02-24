import os
import sys
import soundfile
import librosa  
import numpy as np  
import wave
import json

# Loading config variables
with open('config.json') as f:
    config = json.load(f)

# Loading default normalisation level
default_normalization_level = config['default_normalization_level']

# Loading output path where .pcm will be stored
output_path = config['output_path']

# Loading temp folder where downloaded .pcm will be stored
temp_folder = config['temp_folder']

# Loading if valid .wav should be deleted after being converted to .pcm 
delete_valid_wav_after_pcm_generated = config['delete_valid_wav_after_pcm_generated']

# Resource folder where msupcm.exe and wav2msu.exe are stored
resources_folder = 'src/'

current_path = os.getcwd().replace('\\', '/') + '/'
# For now both folders use temp, can be used to make a difference between raw .wav and converted 
folder_in = temp_folder
folder_out = temp_folder


def create_folder(path):
    """
    Create folder if does not exist
    
    :path: path of directory to create
    """
    if not os.path.exists(path):
        os.mkdir(path)

# Creating output and temp folder
create_folder(output_path)
create_folder(temp_folder)


def convert_wav(path_in, path_out):
    """
    Convert downloaded .wav from smash website to resampled 44.1 KHz .wav
    
    :path_in: path to downloaded .wav
    :path_out: path to output .wav
    """

    y, s = librosa.load(path_in, mono=False, sr=44100) 

    librosa.output.write_wav(path_in, y, 44100)
    wav_16bit(path_in, path_out)
    
    
def wav_16bit(path_in, path_out):
    """
    Convert resampled .wav to 16-bit .wav
    
    :path_in: path to 44.1 KHz .wav
    :path_out: path to output .wav
    """
    data, samplerate = soundfile.read(path_in)
    soundfile.write(path_in, data, 44100, subtype='PCM_16')
    
    # Renaming output .wav to have the same name as input
    try:
        os.rename(path_in, path_out)
    except e:
        os.remove(path_out)
        os.rename(path_in, path_out)
        

def system_command(command):
    """
    Run command. Replace '/' with '\\' for Windows
    
    :command: command to run
    """
    
    if sys.platform.startswith('win'):
        os.system(command.replace('/', '\\\\'))
    else:
        os.system(command)        
    

# Lance depuis script qui telecharge from game ou song. lance la conversion de tout les .wav   
def wav_to_normalized_pcm(folder_final, song_file, sampling_rate, start_loop):
    """
    Convert input .wav to a valid 16-bit 44.1 KHz .wav
    Then, from this valid .wav generate a .pcm and normalize it
    Finally the normalized .pcm is saved in output folder
    
    :folder_final: name of output folder
    :song_file: name .wav file to convert (with extension)
    :sampling_rate: sampling rate of .wav None if no need to loop sound
    :start_loop: start_loop of .wav, uses the sampling rate from parameter sampling_rate
    """
      
    # Path to output folder
    path_final = output_path + folder_final + '/'
    create_folder(path_final)
    
    # Convert .wav to 16-bit-pcm 44.1 KHz
    path_in = current_path + folder_in + '/' + song_file
    path_out = current_path + folder_out + '/' + song_file
    convert_wav(path_in, path_out)

    # Path to valid .wav
    valid_wav_path = current_path + folder_out + '/' + song_file

    # Run process wav2msu.exe in order to generate .pcm
    if sampling_rate is not None:
        # With looping
        start_loop = int(start_loop) * 44.1 / (float(sampling_rate)/ 1000)

        system_command(resources_folder + 'wav2msu.exe "{}" -l {}'.format(valid_wav_path, int(start_loop)))
    else:
        # Without looping
        system_command(resources_folder + 'wav2msu.exe "{}"'.format(valid_wav_path))
    
    # If we delete valid .wav
    if delete_valid_wav_after_pcm_generated:
        os.remove(valid_wav_path)    
    
    # Song name (without '.wav' at the end)
    name = song_file.split('.wav')[0]

    # Defining variables for normalization process
    file_output = '{}.pcm'.format(name)
    path_in = current_path + folder_out + "/" + file_output
    # Temp name for output .pcm
    path_out_normalize = current_path + folder_out + "/out" + file_output
    
    # Run msupcm.exe to normalize .pcm
    system_command(resources_folder + 'msupcm.exe -i "{}" -o "{}" -n {}'.format(path_in, path_out_normalize, default_normalization_level))
    
    # Path to output .pcm
    path_final_normalized = path_final + folder_final + '-' + name + '.pcm'
    
    # Remove input .pcm
    os.remove(path_in)
    # Rename output. pcm to have same name as input .pcm 
    os.rename(path_out_normalize, path_in)
    
    # Move to output folder and replace if exists
    try:
        os.rename(path_in, path_final_normalized)
    except Exception as e:
        print(e)
        os.remove(path_final_normalized)
        os.rename(path_in, path_final_normalized)


def main():
    print("# This script will convert all .wav files from folder '{}' to .pcm files #\n".format(temp_folder))

    # If the script was runned directly without parameters
    if len(sys.argv) < 2:
    
        folder_end = input('> Enter Name of output folder (default: output):\n').replace(' ', '_')
        if folder_end == "":
            print("Using default folder: output")
            folder_end = "output"
            
        sampling_rate = input("> Enter sampling rate in KHz or press Enter if you don't want to loop song:\n")
        if sampling_rate != "":
            sampling_rate = float(sampling_rate)
        
            # start_loop using same sample rate as sampling_rate
            start_loop = float(input("Enter start_loop\n"))
        else:
            sampling_rate=None
            start_loop=None
            
    # If the script was runned directly with parameters sent by the command line interface
    else:
        folder_end = sys.argv[1]
        if len(sys.argv) > 2:
            sampling_rate = float(sys.argv[2])
            start_loop = float(sys.argv[3])
        else:
            sampling_rate=None
            start_loop=None

    # List of .wav inside temp folder
    wav_files = [wav for wav in os.listdir(temp_folder) if ".wav" in wav]

    for wav in wav_files:
        wav_to_normalized_pcm(folder_end, wav, sampling_rate, start_loop)
        
    input("Process complete! .pcm available in folder '{}'. Press enter to finish.\n".format(output_path + folder_end))


if __name__ == "__main__":
    main()