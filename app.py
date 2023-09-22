from flask import Flask, render_template, request
import os
from transcript import VideoTranscriber


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video = request.files['video']
        video.save('temp.mp4')

        media = VideoTranscriber('temp.mp4')
        media.convert_to_audio()
        
        transcript = media.transcribe()

        print(transcript)


        return render_template('result.html', transcript=transcript)

    return render_template('index.html')


app.run(debug=True)