import logging
from datetime import datetime
from os.path import isfile

from app import db

class Settings(db.Model):
    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(64), index=True, unique=True)
    value = db.Column(db.String(120))

    def __repr__(self):
        return '<Setting {}: {}>'.format(self.name, self.value)

class Library(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    title     = db.Column(db.String(128), index=True, unique=True)
    bitrate   = db.Column(db.String(5))
    path      = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Library {}>'.format(self.title)

class Artist(db.Model):
    id     = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return '<Artist {}>'.format(self.name)

class Album(db.Model):
    id     = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return '<Album {}>'.format(self.name)

class Genre(db.Model):
    id     = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return '<Genre {}>'.format(self.name)

def get_config():
    default_config = {
        'download_dir': 'downloads',
        'ffmpeg_binary': 'ffmpeg.exe'
    }
    try:
        config = Settings.query.get(1)
        if config is None:
                logging.debug("Initializing Settings database table")
                config = Settings(download_dir=default_config['download_dir'], ffmpeg_binary=default_config['ffmpeg_binary'])
                db.session.add(config)
                db.session.commit()
                return get_config()
        else:
            logging.debug("Returning Settings")
        return config
    except:
        logging.warn("Settings table does not exist")
        pass

