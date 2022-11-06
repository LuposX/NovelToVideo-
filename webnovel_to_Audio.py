import os
from pydub import AudioSegment
import subprocess
import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='This, transform a text into a mp4 file, which consists of an image and the spoken text.')

# Required positional argument
parser.add_argument('--inference_text_file_name', type=str, default="inference_text",
                    help='The name of the file we want to use to genrate the audio file')

parser.add_argument('--number_of_files_splits', type=int,default=2,
                    help='Set this normally to 1, if you dont have enough VRAM increase the number until it works')

parser.add_argument('--number_of_iterations', type=int, default=12,
                    help='Can be, 2, 6, 12 how many steps the model does. Standard: 12')   

parser.add_argument('--input_image_name', type=str, default="inference_img.jpg",
                    help='Name of the image file that is used in the video')         

parser.add_argument('--output_video_name', type=str, default="inference.mp4",
                    help='Name of the output video')              

args = parser.parse_args()

fileToOpen = args.inference_text_file_name
numberIteration = args.number_of_iterations
numberOfFiles = args.number_of_files_splits

audioExportFolder = "checkpoints/priorgrad/inference_fast" + str(numberIteration) + "_1000000/wavs/" # dont change

image_file = args.input_image_name
video_file_Export = args.output_video_name

# create output directory
try:
    os.makedirs("output")
except FileExistsError:
    # directory already exists
    pass
    
try:
    os.makedirs("output/audio")
except FileExistsError:
    # directory already exists
    pass


# remove old path
try:
    os.rmdir("checkpoints/priorgrad/inference_fast" + str(numberIteration)+ "_1000000")
except OSError as e:
    print("Error: while trying to delete old folder")

# remove weird symbols
with open(fileToOpen + ".txt", "r", encoding='utf-8') as file:
    data = file.read().rstrip()
    data = data.replace("\n", " ")
    data = data.replace("\"", "")
    data = data.replace("\'", "")
    data = data.replace("...", " ")
    data = data.replace(u"\u2018", "'").replace(u"\u2019", "'")


# split the file in multiple smaller files
sentencesList = data.split(".")

# remove empty entries
sentencesList = list(filter(None, sentencesList))

# add back the ".", only when it doesnt alreday have a "."
for i in range(0, len(sentencesList)):
    if (sentencesList[i][-1] != "."):
        sentencesList[i] = sentencesList[i] + "." 

numberOfSentences = len(sentencesList)

numberSentencesPerFile = round(numberOfSentences / numberOfFiles)

for i in range(0, numberOfFiles):
    with open("output/"+ fileToOpen + str(i) + "_edited.txt", "w", encoding='utf-8') as file:
        if (numberSentencesPerFile * (i+1) < numberOfSentences):
            file.write("".join(sentencesList[i * numberSentencesPerFile: (i + 1) * numberSentencesPerFile]))
        else:
            file.write("".join(sentencesList[i * numberSentencesPerFile:]))


# creates the audio files
for i in range(0, numberOfFiles):
    filename = "inference_text"+ str(i) +"_edited.txt"
    print("------------------------------------------------------------------")
    print("Current File: " + filename)
    print("------------------------------------------------------------------")
    os.system("CUDA_VISIBLE_DEVICES=0 PYTHONPATH=. python tasks/priorgrad_inference.py --config configs/tts/lj/priorgrad.yaml --exp_name priorgrad --reset --inference_text " + "output/" + filename + " --fast --fast_iter " + str(numberIteration))
    
    # rename the file so that we thats it sortet
    singleAudioFile = [f for f in os.listdir(audioExportFolder) if os.path.isfile(os.path.join(audioExportFolder, f))]
    os.rename(audioExportFolder + singleAudioFile[0], "output/audio/part" + str(i) + ".mp3")
    

# Get all audio files and combine to one
onlyfiles = [f for f in os.listdir("output/audio/") if os.path.isfile(os.path.join("output/audio/", f))]
onlyfiles = sorted(onlyfiles)
print("Number of audio files to be added: " + str(len(onlyfiles)))

completeAudio = AudioSegment.empty()
for i in range(0, len(onlyfiles)):
    print("Audio file name: " + onlyfiles[i])
    completeAudio += AudioSegment.from_file("output/audio/" + onlyfiles[i], format="wav");
    
completeAudio.export("output/combinedAudio.mp3", format="mp3")

 # audio.mp3 + image.jpg = video.mp4
mp3_file = "output/combinedAudio.mp3"
if image_file == "":
    print("no image")
else:
    subprocess.call([
        "ffmpeg", "-r", "1", "-loop", "1", "-y", "-i", image_file, "-i", mp3_file, "-c:a", "copy", "-r", "1", "-vcodec", "libx264", "-shortest", "output/" + video_file_Export
    ])


