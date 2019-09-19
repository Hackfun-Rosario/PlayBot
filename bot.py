#!/usr/bin/env python3

from urllib.parse import urlparse
from pathlib import Path
from os import environ as env
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

allow = ["youtu.be", "youtube.com", "www.youtube.com"]

## telegram updater and dispatcher
updater = Updater(env["BOT_KEY"], use_context=True)
dispatcher = updater.dispatcher

## parse url and add file to playlist if allowed
def check_url(url):
  ## parse url
  u = urlparse(url)
  vid = ""
  ## check if the url is what we want
  if u.netloc in allow:
    #get video id (vid)
    if u.path == '/watch':
      vid = u.query.split("v=")[1].split("&")[0]
    else:
      vid = u.path[1:]
    #touch file
    # Path('playlist/{}'.format(vid)).touch()
    with open("site/play.list", "a") as f:
      f.write(vid+"\n")

## message handler
@run_async
def add_to_playlist(update, context):
  check_url(update.message.text)

playlist_handler = MessageHandler(Filters.entity("url"), add_to_playlist)
dispatcher.add_handler(playlist_handler)

## listen and iterate
updater.start_polling()
updater.idle()