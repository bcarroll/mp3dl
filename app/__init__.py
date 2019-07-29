import logging
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify
from flask import flash
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from os import urandom
from os.path import abspath
from os.path import dirname
from os.path import join as path_join
from os.path import isfile

from youtube_api import YoutubeGAPI

logging.basicConfig(level=logging.DEBUG)

basedir = abspath(dirname(__file__))

config = {'download_dir': abspath(path_join(basedir, '..', 'downloads')), 'ffmpeg_binary': path_join(basedir, 'ffmpeg.exe')}

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path_join(basedir, 'data.dat')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
import db
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