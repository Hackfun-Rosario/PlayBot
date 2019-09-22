#!/usr/bin/env python3

from flask import Flask, Response, send_from_directory
from threading import Thread
import hashlib

cks = None

## CHECKSUM THREAD
def ck_fun():
  global cks
  while True:
    with open("site/play.list","r") as f:
      cks = hashlib.md5(f.read().encode('utf-8')).hexdigest()

ck = Thread(target=ck_fun)
ck.setDaemon(True)
ck.start()


## WEB APP SERVER
app = Flask(__name__, static_url_path='')

@app.route('/event_stream')
def stream():
  def event_stream():
    global cks
    h = None
    while True:
      if (cks != h):
        h = cks
        yield 'event: update\ndata: %s\n\n' % h
  return Response(event_stream(), mimetype="text/event-stream")

@app.route('/list')
def playlist():
  return send_from_directory('site','play.list', mimetype="text/plain")

@app.route('/')
def main():
  return send_from_directory('site','index.html')


## RUN SERVER
if __name__ == '__main__':
  app.run(port=8080)
