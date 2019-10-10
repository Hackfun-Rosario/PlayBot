#!/usr/bin/env python3

from flask import Flask, Response, send_from_directory
from multiprocessing.managers import BaseManager
from multiprocessing import Process, Value
from time import sleep
import hashlib


## thread para avisar que hay nuevos elementos en la playlist
# clase del manager para hablar con el broker
class QMan(BaseManager):
  pass

# registramos el metodo de la queue
QMan.register('get_queue')

## conectamos con el servicio e inicializamos la queue
m = QMan(address=('localhost', 60606), authkey=b'cambiame la key')
m.connect()
q = m.get_queue()

## esta es la funcion que recibe el mensaje de actualizacion
#  corre en un loop "eterno"
def update_playlist(data,queue):
  while True:
    if not queue.empty():
      data.value = queue.get()

# flag del update
upd = Value('d', 0.0)


## WEB APP SERVER
app = Flask(__name__, static_url_path='')

@app.after_request
def add_header(r):
  # Desactivamos la cache, porque si no nos carga siempre la misma playlist
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
        old = upd.value
        yield 'event: update\ndata: do it!\n\n'
      sleep(2)
  # return response
  return Response(event_stream(), mimetype="text/event-stream")

## endpoint de la playlist. por ahora levanta un archivo solo.
#  TODO: adaptar para tener muchas playlists
@app.route('/list')
def playlist():
  return send_from_directory('site','play.list', mimetype="text/plain")

## endpoint del index!!!
@app.route('/')
def main():
  return send_from_directory('site','index.html')


## RUN SERVER
if __name__ == '__main__':
  # iniciamos el subproceso como daemon
  p = Process(target=update_playlist, args=(upd,q))
  p.daemon = True
  p.start()
  # arrancamos el server web (brummm brummm!!)
  app.run(port=8080)
