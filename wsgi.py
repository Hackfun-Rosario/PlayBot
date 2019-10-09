#!/usr/bin/env python3

from flask import Flask, Response, send_from_directory
from multiprocessing.managers import BaseManager
from multiprocessing import Process, Value
from time import sleep
import hashlib


## update thread
# create class
class QMan(BaseManager):
  pass

# register queue method
QMan.register('get_queue')

## run service
m = QMan(address=('localhost', 60606), authkey=b'cambiame la key')
m.connect()

q = m.get_queue()

## esta es la funcion que recibe el mensaje de actualizacion
def update_playlist(data,queue):
  while True:
    if not queue.empty():
      print("value received")
      data.value = queue.get()

upd = Value('d', 0.0)# update flag


## WEB APP SERVER
app = Flask(__name__, static_url_path='')

@app.after_request
def add_header(r):
  # Desactivamos la cache
  r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
  r.headers["Pragma"] = "no-cache"
  r.headers["Expires"] = "0"
  r.headers['Cache-Control'] = 'public, max-age=0'
  return r


@app.route('/event_stream')
def stream():
  def event_stream():
    old = None
    while True:
      # comparamos si hubo algun cambio en el valor de upd
      if upd.value != old:
        print("nuevo valorrrr")
        old = upd.value
        yield 'event: update\ndata: do it!\n\n'
      sleep(2)
  # return response
  return Response(event_stream(), mimetype="text/event-stream")

@app.route('/list')
def playlist():
  return send_from_directory('site','play.list', mimetype="text/plain")

@app.route('/')
def main():
  return send_from_directory('site','index.html')


## RUN SERVER
if __name__ == '__main__':
  # iniciamos el subproceso como daemon
  p = Process(target=update_playlist, args=(upd,q))
  p.daemon = True
  p.start()
  # start server
  app.run(port=8080)
