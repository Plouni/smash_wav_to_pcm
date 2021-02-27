# smash_wav_to_pcm

Download brstm files from https://smashcustommusic.net that you can use to create a MSU pack with.  
Why this website? Because it has looping points for most of the songs!  
So you can either use `Looping Audio Converter` (https://github.com/libertyernie/LoopingAudioConverter) to convert these brstm files to looped pcm files or you can just let some Python libraries handle this conversion automatically.  


## Requirements
To download the songs, you'll need to have Python 3 installed with the following libraries:
* `requests`
* `bs4`
* `urllib`

And if you are not using `Looping Audio Converter` you'll also need these:
* `soundfile`
* `numpy`
* `librosa == 0.6.0` (it won't work with above versions)


## Project structure
.  
|_ lib/  
  |_ `__init__.py`  
  |_ `functions.py`   
|_ output_pcm/  
|_ tools/  
  |_ `msupcm.exe`  
  |_ `wav2msu.exe`  
  |_ `VGAudioCli.exe`  
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
  * `VGAudioCli.exe` is used here to convert a brstm file to a wav file
  * `msupcm.exe` is used here to normalize the level of a pcm file
  * `wav2msu.exe` is used here to convert a wav file to a pcm file
* temp: temporary folder where downloaded wav and generated pcm will be stored. Will be automatically created

It is also important to have the config and all python files at the root of the project or it won't work.


## How to use
By default, the script will only download the brstm files. If you want to convert automatically the brstm to wav without using `Looping Audio Converter`, you'll have to check the config file to set `auto_convert_brstm_to_pcm` to `true`.  

### Simple Usage
The easiest way is to simply click the Python scripts. They all have different uses:
* `download_from_id_song.py`: asks for a song id from smashcustommusic.net and will download the brstm file. (Can also convert it to a pcm file)
* `download_song_from_id_game.py`: asks for a game id from smashcustommusic.net and will download all of the brstm files. (Can also convert them to a pcm file)
* `generate_pcm_from_wav.py`: asks for a wav file (or folder) and will transform it to a 16bit 44.1KHz wav, convert it to a pcm and then normalize it

To get the game id from smashcustommusic.net, take the number at the end of the URL of a game.  
For example: `Zelda ALTTP` URL is https://smashcustommusic.net/game/95 ==> game ID is `95`

To get the song id from smashcustommusic.net, take the number at the end of the URL of a song.  
For example: `Zelda ALTTP Castle Theme` URL is https://smashcustommusic.net/song/11816 ==> song ID is `11816`

### Command line Usage
You can also run the Python script with the command line by using:  
`python name_of_python_script.py param1 param2 param3`  
But by doing this, you have to enter the parameters in the right order. Here is the order for each script:
* `download_from_id_song.py`: song id from `smashcustommusic.net`, output folder (`optional`, root of output_folder defined in config file by default)
* `download_song_from_id_game.py`: game id from `smashcustommusic.net`, output folder (`optional`, root of output_folder defined in config file by default)
* `generate_pcm_from_wav.py`: output folder, sampling rate (`optional`, if multiple songs, will be used for all of them), start looping point (optional, requires sampling rate. If multiple songs, will be used for all of them)


## Config file
Here are the settings you can customize in the config file:
* `output_path`: path to output folder where pcm files will be stored
* `stop_words`: list of "stop words". Any song that contains any of the "stop words" won't be downloaded (if you want to exclude remixes for example)
* `temp_folder`: path to temp
* `tools_folder`: path to tools folder

Use these only if you're not using `Looping Audio Converter` and prefer to handle the brstm to pcm conversion automatically with Python: 
* `auto_convert_brstm_to_pcm`: set it to `false` if you are using `Looping Audio Converter`, `true` otherwise (you'll need the required librairies, check the `Requirements` section)
* `default_normalization_level`: normalization level that will be used by `msupcm.exe`. Default: -21
* `delete_valid_wav_after_pcm_generated`: if you want to delete 16bit 44.1KHz wav files after the pcm file has been generated. Default: `true`


## Credits
qwertymodo is the creator of `msupcm.exe`  
jbaiter is the creator of `wav2msu.exe`
