# smash_wav_to_pcm

Download brstm files from https://smashcustommusic.net that you can use to create an MSU pack with.  
Why this website? Because it has looping points for most of the songs!  
You also need to download the powerful tool `Looping Audio Converter` to convert the brstm files to looped pcm files. You don't need to know how to use this tool, because the config files are given to you and the process is called automatically by python and the command line interface of Looping Audio Converter. 


## Requirements
To download the songs, you'll need to have Python 3 installed with the following libraries:
* `requests`
* `bs4`
* `urllib`

To convert wav to pcm files, this project uses :
* `Looping Audio Converter`, you can get it here : (https://github.com/libertyernie/LoopingAudioConverter)


## Project structure
.  
|_ lib/  
  |_ `__init__.py`  
  |_ `functions.py`   
|_ output/  
|_ tools/  
  |_ `msupcm.exe`  
  |_ `VGAudioCli.exe`  
  |_ `wav_44100.xml`  
  |_ `wav_to_pcm.xml`
|_ temp/  
|_ `config.json`  
|_ `download_from_id_song.py`  
|_ `download_song_from_id_game.py`  
|_ `generate_pcm_from_wav.py`  
|_ `Readme.md`  

Folder details:
* lib: folder that contains common functions used by the python scripts
* output_pcm: default folder where output .pcm will be stored. Will be automatically created
* tools:
  * `msupcm.exe` is used here to normalize the level of a pcm file
  * `VGAudioCli.exe` is used here to convert a brstm file to a wav file
  * `wav_44100.xml` is the config file that will be used by Looping Audio Converter to automatically resample a song to 44.1 KHz
  * `wav_to_pcm.xml` is the config file that will be used by Looping Audio Converter to automatically convert any wav to a pcm file
  * `wav2msu.exe` is used here to convert a wav file to a pcm file
* temp: temporary folder where downloaded wav and generated pcm will be stored. Will be automatically created

It is also important to have the config and all python files at the root of the project or it won't work.


## How to use

### Simple Usage
The easiest way is to simply click the Python scripts. They all have different uses:
* `download_from_id_song.py`: asks for a song id from smashcustommusic.net and will download the brstm file and convert it to a pcm file
* `download_song_from_id_game.py`: asks for a game id from smashcustommusic.net and will download all of the brstm files and convert them to pcm files
* `generate_pcm_from_wav.py`: transforms wav files inside the temp folder to normalized pcm

To get the game id from smashcustommusic.net, take the number at the end of the URL of a game.  
For example: `Zelda ALTTP` URL is https://smashcustommusic.net/game/95 ==> game ID is `95`

To get the song id from smashcustommusic.net, take the number at the end of the URL of a song.  
For example: `Zelda ALTTP Castle Theme` URL is https://smashcustommusic.net/song/11816 ==> song ID is `11816`

### Command line Usage
You can also run the Python script with the command line by using:  
`python name_of_python_script.py param1 param2 param3`  
But by doing this, you have to enter the parameters in the right order. Here is the order for each script:
* `download_from_id_song.py`: song id, output folder (optional, root of output_folder defined in config file by default)
* `download_song_from_id_game.py`: game id, output folder (optional, root of output_folder defined in config file by default)
* `generate_pcm_from_wav.py`: output folder, start looping point (optional).


## Config file
Here are the settings you can customize in the config file:
* `looping_audio_converter_path`: path to where your Looping Audio Converter is located on your PC. You must fill this or the program won't work

* `output_path`: path to output folder where output files will be stored
* `stop_words`: list of "stop words". Any song that contains any of the "stop words" won't be downloaded (if you want to exclude remixes for example)
* `temp_folder`: path to temp
* `tools_folder`: path to tools folder
* `looping_config_wav_to_pcm`: path to config files for Looping Audio Converter
* `default_normalization_level`: normalization level that will be used by `msupcm.exe`. Default: -21
* `delete_valid_wav_after_pcm_generated`: if you want to delete the 16bit 44.1KHz wav file after the pcm file has been generated. Default: `true`


## Credits
qwertymodo is the creator of `msupcm.exe`
Thealexbarney is the creator of `VGAudioCli.exe`