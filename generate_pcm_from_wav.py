import os
import sys
import json
import wave
import array
from lib.functions import system_command, get_folder_final_info

# Loading config variables
with open('config.json') as f:
    config = json.load(f)

# Loading default normalisation level
default_normalization_level = config['default_normalization_level']

# Loading parent output folder where .pcm will be stored
output_path = config['output_path']

# Name of track config file
tracks_file = config['tracks_file']

# Loading temp folder where downloaded .pcm will be stored
temp_folder = config['temp_folder']

# Loading if valid .wav should be deleted after being converted to .pcm 
delete_valid_wav_after_pcm_generated = config['delete_valid_wav_after_pcm_generated']

# Loading tools folder where msupcm.exe and wav2msu.exe are stored
tools_folder = config['tools_folder']

# Loading folder to config files for looping audio converter
looping_config_wav_to_pcm = config['looping_config_wav_to_pcm']

# Loading folder for looping audio converter
looping_audio_converter_path = config['looping_audio_converter_path']

current_path = os.getcwd().replace('\\', '/') + '/'
# For now both folders use temp, can be used to make a difference between raw .wav and converted 
folder_in = temp_folder
folder_out = temp_folder

# By default debug is False unless run directly by main
debug = False


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


def check_and_make_stereo(file1, output):
    """
    Check if song is mono and convert it to stereo if that's the case
    
    :file1: input file
    :output: name of pcm output file
    """
    ifile = wave.open(file1)
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = ifile.getparams()
    
    if nchannels == 1:
    
        array_type = {1:'B', 2: 'h', 4: 'l'}[sampwidth]
        left_channel = array.array(array_type, ifile.readframes(nframes))[::nchannels]
        ifile.close()

        stereo = 2 * left_channel
        stereo[0::2] = stereo[1::2] = left_channel

        ofile = wave.open(file1, 'w')
        ofile.setparams((2, sampwidth, framerate, nframes, comptype, compname))
        ofile.writeframes(stereo.tobytes())
        ofile.close()


def wav_to_pcm_with_loopingaudioconverter(start_loop, wav_file, file_output):
    """
    Create pcm file from wav using loopingaudioconverter
    
    :start_loop: start_loop of .wav
    :wav_file: name .wav file to convert (with extension)
    :file_output: name of pcm output file
    """

    # Get number of samples
    wav_song = wave.open(wav_file, 'rb')
    end_loop = wav_song.getnframes()
    wav_song.close()
    
    if start_loop is not None:
        # Overwrite looping points file
        with open('loop.txt', 'w') as f:
            f.write("{} {} {}".format(int(start_loop), end_loop, wav_file))
    
    config_file = 'wav_to_pcm.xml'
    if config_file not in os.listdir(current_path + looping_config_wav_to_pcm):
        input('{} not found! Check if you have this file or download the project again...'.format(current_path + looping_config_wav_to_pcm + config_file))
        return 0
    
    # Convert wav to .pcm using LoopingAudioConverter
    system_command('LoopingAudioConverter.exe {} {} --auto'.format(current_path + looping_config_wav_to_pcm+config_file, wav_file))

    path_in = current_path + folder_out + file_output
    os.rename(file_output, path_in)
  
    # If we delete valid .wav
    if delete_valid_wav_after_pcm_generated:
        os.remove(wav_file)
    
    return path_in
    

# Lance depuis script qui telecharge from game ou song. lance la conversion de tout les .wav   
def wav_to_normalized_pcm(folder_final, wav_file, start_loop):
    """
    Convert input .wav to a valid 16-bit 44.1 KHz .wav
    Then, from this valid .wav generate a .pcm and normalize it
    Finally the normalized .pcm is saved in output folder
    
    :folder_final: name of output folder
    :wav_file: name .wav file to convert (with extension)
    :start_loop: start_loop of .wav
    """
    
    # Get path to output folder and prefix to output file
    path_folder_final, prefix_file_final = get_folder_final_info(output_path, folder_final)
    create_folder(path_folder_final)

    # Nom fichier sans extension 
    name = wav_file.split('.wav')[0]
    # Defining variables for normalization process
    file_output = '{}.pcm'.format(name)
    
    
    # Change dir to looping_audio_converter_path
    os.chdir(looping_audio_converter_path)
    
    # Check if stereo or convert it
    check_and_make_stereo(wav_file, wav_file)

    # Create pcm file
    path_in = wav_to_pcm_with_loopingaudioconverter(start_loop, wav_file, file_output)
    
    # Temp name for output .pcm
    path_out_normalize = current_path + folder_out + "out" + file_output
    
    # Change back to current_path
    os.chdir(current_path)
    
    
    # Run msupcm.exe to normalize .pcm
    system_command(tools_folder + 'msupcm.exe -i "{}" -o "{}" -n {}'.format(path_in, path_out_normalize, default_normalization_level), debug)
    
    # Path to output .pcm
    path_final_normalized = path_folder_final + prefix_file_final + name + '.pcm'
    
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
        
# Clean start loop
def parse_start_loop(start_loop):
    if start_loop != "" and start_loop != "json":
        return float(start_loop)
        
    elif start_loop != "json":
        return None
        
    return start_loop


def main():
    print("# This script will convert all .wav files from folder '{}' to .pcm files #\n".format(temp_folder))
    
    debug = True
    
    if not os.path.exists(looping_audio_converter_path) or "LoopingAudioConverter.exe" not in os.listdir(looping_audio_converter_path):
        input("Error because LoopingAudioConverter.exe not found! Please make sure 'looping_audio_converter_path' in the config file is correct!")
        return 0
    

    # If the script was runned directly without parameters
    if len(sys.argv) < 2:
    
        folder_end = input('> Enter Name of output folder:\n').replace(' ', '_')
            
        # Number of samples in smash website
        start_loop = input("> Enter start loop point:\n - as a number of samples\n - 'json' (without quotes) if using a file inside {}\n - just press Enter if no looping.\n".format(temp_folder))
        start_loop = parse_start_loop(start_loop)
            
    # If the script was runned directly with parameters sent by the command line interface
    else:
        folder_end = sys.argv[1]
        if len(sys.argv) > 2:
            parse_start_loop(start_loop)
        else:
            start_loop=None

    # List of .wav inside temp folder
    wav_files = [wav for wav in os.listdir(temp_folder) if ".wav" in wav]

    if len(wav_files) == 0:
        input("No .wav files found inside folder {}. Press enter to finish.\n".format(temp_folder))

    else:
    
        tracks=None
        if tracks_file in os.listdir(temp_folder) and start_loop == 'json':
            with open(temp_folder + tracks_file, 'r') as f:
                tracks = json.load(f)

    
        for wav in wav_files:
            if ' ' in wav:
                wav_clean = wav.replace(' ', '_')
            else:
                wav_clean = wav
                
            # Loads from json
            if tracks is not None:
                track_number = wav.split('-')[1].split('.')[0]
                start_loop = tracks[track_number]["Start_loop"]
                if len(start_loop) == 0:
                    start_loop = None
                
            os.rename(temp_folder + wav, looping_audio_converter_path + wav_clean)
                
            wav_to_normalized_pcm(folder_end, wav_clean, start_loop)
            
        input("Process complete! .pcm available in folder '{}'. Press enter to finish.\n".format(output_path + folder_end))


if __name__ == "__main__":
    main()