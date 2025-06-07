from flask import Flask, render_template, request
from transcript import Transcriber, runner

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        file = request.files['file']
        media_type = file.content_type.split("/")
        file_name = 'temp.' + media_type[1]
        file.save(file_name)
        print("media : ",media_type)
        media = Transcriber(file_name)
        transcript = runner(media, media_type)
        
        s=''
        for i in transcript : 
            s = s + i + ' '
        transcript = s
        text = open(r"templates/trans.txt","w+")
        text.write(transcript)
        text.close()
        
        return render_template('result.html', transcript=transcript)

    return render_template('index.html')

@app.route('/summ')
def summ():
    import backend.offline as offline
    with open(r'summ.txt', 'r+') as file:
        summary = file.read()
    return render_template('summ.html', summary = summary )

@app.route('/game')
def game():
    return render_template('game.html')

app.run(debug=True)