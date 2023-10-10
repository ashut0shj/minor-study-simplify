from flask import Flask, render_template, request
from transcript import Transcriber

'''todo add mime'''

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        video = request.files['video']
        media_type = video.content_type.split("/")
        file = 'temp.' + media_type[1]
        video.save(file)

        media = Transcriber(file)

        #if media_type[0] == 'video':
        input("Press enter to continue with transcription")
        
        transcript = media.video_transcribe()
        print(transcript)

        return render_template('result.html', transcript=transcript)

    return render_template('index.html')


app.run(debug=True)