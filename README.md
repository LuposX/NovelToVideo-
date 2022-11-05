# NovelToVideo-
> A script which can be used in combination to NeuralSpeech, to transform a text and an additional image to and video.

## Installation
1. Clone `microsoft/NeuralSpeech`
2. and follow their guide to install `PriorGrad-acoustic`
3. Install [ffmpeg](https://ffmpeg.org/)
4. Clone this project, install the requirements via `pip install -r requirements.txt`

## Usage
1. Run `python webnovel_to_Audio.py`  
2. If you get a memory error run the command with `--split 2` increase the number until you dont get a error anymore
3. the files will be in the `output/` folder
