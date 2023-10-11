from flask import Flask, render_template, request
from transcript import Transcriber

'''todo add mime'''

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        file = request.files['file']
        media_type = file.content_type.split("/")
        file_name = 'temp.' + media_type[1]
        file.save(file_name)

        media = Transcriber(file_name)

        #if media_type[0] == 'video':
        #input("Press enter to continue with transcription")
        
        transcript = media.image_transcribe()
        media.printt()

        return render_template('result.html', transcript=transcript)

    return render_template('index.html')


app.run(debug=True)