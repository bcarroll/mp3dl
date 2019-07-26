from flask import Flask, render_template, request, url_for, jsonify
from config import youtube_apikey
from youtube_api import YoutubeAPI

from os.path import isdir, isfile

config = {
        'api_key': youtube_apikey,
        'download_dir': 'downloads'
    }

app = Flask(__name__)
yt = YoutubeAPI(key=youtube_apikey)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if config['api_key'] is None or config['api_key'] == "":
            return render_template('settings.html', settings=config)
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

@app.route('/validate_config', methods=['GET'])
def validate_config():
    return jsonify(config)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1025, debug=True)
