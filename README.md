# NovelToVideo-
> A script which can be used in combination to NeuralSpeech, to transform a text and an additional image to and video.

This program is for people who like to read webnovels and other forms of books and want an audiobook for their favourite Novel/Book.
This script translates an text-to-Speech and you get an audio files.
Additonally you can provide an Iamge and the audio files and image get put together to form a video which can be uploaded.
For example [look here.](https://youtu.be/5hf_aVKSaM8)

## Installation
1. Clone `microsoft/NeuralSpeech`
2. and follow their guide to install `PriorGrad-acoustic`
3. Install [ffmpeg](https://ffmpeg.org/)
4. Clone this project, install the requirements via `pip install -r requirements.txt`

## Usage
1. Write in `inference_text.txt`, which lies in the `PriorGrad-acoustic` folder, the etxt you want to transform to speech
2. put an image in the same folder with the name of `inference_img.jpg` which will be the standstill image for the video
3. Run `python webnovel_to_Audio.py`  
4. If you get a memory error run the command with `--number_of_files_splits 4` increase the number until you dont get a error anymore
5. the files will be in the `output/` folder
