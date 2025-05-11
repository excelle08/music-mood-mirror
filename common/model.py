# -*- coding: utf-8 -*-
import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Model = db.Model


def to_dict(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your conversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__dict__.keys():
        if c.startswith('_'):
            continue
        v = getattr(inst, c)
        if type(v) in convert.keys() and v is not None:
            try:
                d[c] = convert[c.type](v)
            except:
                d[c] = "Error:  Failed to covert using ", str(convert[type(v)])
        elif v is None:
            d[c] = str()
        else:
            d[c] = v
    return d


def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__dict__.keys():
        if c.startswith('_'):
            continue
        v = getattr(inst, c)
        if type(v) in convert.keys() and v is not None:
            try:
                d[c] = convert[c.type](v)
            except:
                d[c] = "Error:  Failed to covert using ", str(convert[type(v)])
        elif v is None:
            d[c] = str()
        else:
            d[c] = v
    return json.dumps(d)


class Base():

    def __init__(self):
        pass

    @property
    def json(self):
        return to_json(self, self.__class__)

    @property
    def dict(self):
        return to_dict(self, self.__class__)



class Song(Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    artist = db.Column(db.String(256), nullable=False)
    album = db.Column(db.String(256))
    play_datetime = db.Column(db.DateTime)
    result_title = db.Column(db.String(256))
    result_artist = db.Column(db.String(256))
    result_album = db.Column(db.String(256))
    duration = db.Column(db.Integer)
    lyrics = db.Column(db.Text)
    synced_lyrics = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "play_datetime": self.play_datetime.isoformat() if self.play_datetime else None,
            "result_title": self.result_title,
            "result_artist": self.result_artist,
            "result_album": self.result_album,
            "duration": self.duration,
            "lyrics": self.lyrics,
            "synced_lyrics": self.synced_lyrics
        }
