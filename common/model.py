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
            except Exception:
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
            except Exception:
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


class User(Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


class ListenHistory(Model):
    __tablename__ = 'listen_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    artist = db.Column(db.String(256), nullable=False)
    album = db.Column(db.String(256))
    play_datetime = db.Column(db.DateTime)
    result_title = db.Column(db.String(256))
    result_artist = db.Column(db.String(256))
    result_album = db.Column(db.String(256))
    lyrics = db.Column(db.Text)
    synced_lyrics = db.Column(db.Text)
    duration = db.Column(db.Integer)
    seconds_played = db.Column(db.Integer)
    music_completion_rate = db.Column(db.Float)
    reason_start = db.Column(db.String(64))
    reason_end = db.Column(db.String(64))
    shuffle = db.Column(db.Boolean, default=False)
    skip = db.Column(db.Boolean, default=False)
    week = db.Column(db.Integer)
    first_occurrence_in_week = db.Column(db.Boolean, default=False)
    repeats_this_week = db.Column(db.Integer)
    repeats_next_7d = db.Column(db.Integer)
    
