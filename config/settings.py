#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# config/settings.py
# This file contains the configuration settings for the application.

LRCLIB_SITE = "https://lrclib.net/"
# You can set LRC_LIB_SITE to a local server if you are able to
# launch the LRCLIB server locally by following the instructions at
# https://github.com/tranxuanthang/lrclib
# LRCLIB_SITE = "http://127.0.0.1:3300"
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "password"
DB_NAME = "music"
MYSQL_DB_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLITE_DB_URI = "sqlite:///data/music.db"
