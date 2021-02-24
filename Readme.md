# smash_wav_to_pcm

Generate pcm files from songs found in smashcustommusic.net  
Why this website? Because it has looping points for almost every song! And with Python it's easy to download the song, retrieve the looping points and use it to generate a pcm file! 


## Requirements
You need to have Python 3 installed with the following libraries:
* requests
* bs4
* urllib
* soundfile
* numpy
* librosa == 0.6.0 (it won't work with above versions!)


## Project structure
.  
|_ output_pcm  
|_ src  
  |_ msupcm.exe  
  |_ wav2msu.exe  
|_ temp  
|_ config.json  
|_ download_from_id_song.py  
|_ download_song_from_id_game.py  
|_ generate_pcm_from_wav.py  
|_ Readme.md  

Folder details:
* output_pcm: default folder where output .pcm will be stored. Will be automatically created.
* src:
  * msupcm.exe is used here to normalize the level of a pcm file
  * wav2msu.exe is used here to convert a wav file to a pcm file
* temp: temporary folder where downloaded wav and generated pcm will be stored. Will be automatically created.

It is also important to have the config and all python files at the root of the project or it won't work!


## How to use
The easiest way is to simply click the Python scripts. They all have different uses:
* download_from_id_song.py: asks for a song id from smashcustommusic.net and will generate a pcm file
* download_song_from_id_game.py: asks for a game id from smashcustommusic.net and will generate a pcm file for all songs from this game
* generate_pcm_from_wav.py: asks for a wav file (or folder) and will transform it to a 16bit 44.1KHz wav, convert it to a pcm and then normalize it

To get the game id from smashcustommusic.net, take the number at the end of the URL of a game.  
For example, the URL for Zelda ALTTP is https://smashcustommusic.net/game/95 so the game ID is 95

To get the song id from smashcustommusic.net, take the number at the end of the URL of a song.  
For example, the URL for Zelda ALTTP Hyrule Castle is https://smashcustommusic.net/song/11816 so the song ID is 11816,

You can also run the Python script with the command line by using:  
`python name_of_python_script.py` param1 param2 param3  
But by doing this, you have to enter the parameters in the right order.


## Config file
Here are the settings you can customize in the config file:
* output_path: path to output folder where pcm files will be stored
* default_normalization_level: normalization level that will be used by msupcm.exe. Default: -21
* stop_words: list of "stop words". Any song that contains any of the "stop words" won't be downloaded (if you want to exclude remixes for example)
* temp_folder: path to temp folder
* delete_valid_wav_after_pcm_generated: if you want to delete 16bit 44.1KHz wav files after the pcm file has been generated. Default: True


## Credits
qwertymodo is the creator of msupcm.exe  
jbaiter is the creator of wav2msu.exe
