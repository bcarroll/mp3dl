import logging
from flask import Flask, render_template, request, url_for, jsonify, flash, redirect
from youtube_api import YoutubeGAPI
from os import urandom

logging.basicConfig(level=logging.DEBUG)

config = {
        'download_dir': 'downloads',
        'ffmpeg_binary': 'ffmpeg.exe'
    }

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(16)
yt = YoutubeGAPI(config=config)

@app.route('/', methods=['GET', 'POST'])
def index():
    if yt.FFMPEG_BIN is None:
        flash('ffmpeg_binary setting must contain the location of the ffmpeg executable')
        return redirect(url_for('settings', config=config))
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        results=yt.search( request.form['search'] )
        return render_template('index.html', results=results)

@app.route('/favicon.ico')
def favicon(): return ""

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        return render_template('settings.html', settings=config)
    elif request.method == 'POST':
        #TODO: Update config
        return redirect(url_for('settings'))

@app.route('/download/<string:id>', methods=['GET', 'POST'])
def download(id):
    return jsonify( yt.download(id) )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1025, debug=True)
