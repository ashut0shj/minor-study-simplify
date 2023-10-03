import moviepy.editor as mp
import assemblyai as aai
import os

with open("api_key.txt") as file:
    file_content = file.readline()
    api_key = file_content

class VideoTranscriber:

    aai.settings.api_key = api_key

    def __init__(self,video_file_path):
        self.transcriber = aai.Transcriber()
        self.video_file_path = video_file_path
        #this is in it
        

    def convert_to_audio(self):
        video_clip = mp.VideoFileClip(self.video_file_path)
        video_clip.audio.write_audiofile('temp.wav')
        video_clip.close()
        os.remove('temp.mp4')

    def transcribe(self):
        transcript = self.transcriber.transcribe(r"temp.wav")
        os.remove('temp.wav')

        return transcript.text
