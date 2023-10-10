import moviepy.editor as mp
import assemblyai as aai
import os
from PIL import Image 
from pytesseract import pytesseract 

with open("api_key.txt") as file:
    file_content = file.readline()
    api_key = file_content

class Transcriber:

    aai.settings.api_key = api_key

    def __init__(self,video_file_path):
        self.transcriber = aai.Transcriber()
        self.video_file_path = video_file_path
        self.media_type = video_file_path.split(".")[-1]
        print(self.media_type)
        
    
    def audio_transcribe(self):
        transcript = self.transcriber.transcribe(r"temp.wav")
        os.remove('temp.wav')
        print("Transcribing")
        return transcript.text

    def video_transcribe(self):
        video_clip = mp.VideoFileClip(self.video_file_path)
        video_clip.audio.write_audiofile('temp.wav')
        video_clip.close()
        os.remove('temp.mp4')
        print("video converted")
        self.audio_transcribe()
    
    def image_transcribe(self):
        image_path = r"text.png"
        img = Image.open(image_path) 
        text = pytesseract.image_to_string(img) 
        print(text[:-1])

