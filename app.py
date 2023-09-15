from flask import Flask, render_template, request
import moviepy.editor as mp
import assemblyai as aai
import os


aai.settings.api_key = "6633f26c9fc144a38eb407f404483797"
transcriber = aai.Transcriber()

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video = request.files['video']
        video.save('temp.mp4')

        video_clip = mp.VideoFileClip('temp.mp4')
        video_clip.audio.write_audiofile('temp.wav')

        transcript = transcriber.transcribe(r"temp.wav")


        print(transcript.text)

        transcript = transcript.text

        # Delete temporary files
        video_clip.close()
        os.remove('temp.mp4')
        os.remove('temp.wav')

        return render_template('result.html', transcript=transcript)

    return render_template('index.html')


app.run(debug=True)