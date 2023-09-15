import moviepy.editor as mp
import assemblyai as aai

print(1)

aai.settings.api_key = "6633f26c9fc144a38eb407f404483797"

transcriber = aai.Transcriber()
print("API connected")

#video address
vid = (r"C:\Users\ashut\Downloads\y2mate.com - Ed Sheeran  Happier Official Music Video_v240P.mp4")

print("converting vid to audio")
video_clip = mp.VideoFileClip(vid)
video_clip.audio.write_audiofile('temp.wav')

#transcribing audio
transcript = transcriber.transcribe(r"temp.wav")


print(transcript.text)