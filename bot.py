#!/usr/bin/env python3

from urllib.parse import urlparse
from pathlib import Path
from os import environ as env
from telegram.ext import Updater, CommandHandler
from telegram.ext.dispatcher import run_async
# multiprocessing block
from multiprocessing.managers import BaseManager
from time import time

# creamos la clase para interactuar con el broker
class QMan(BaseManager):
  pass

# registramos el metodo para la queue
QMan.register('get_queue')

## conectamos con el servicio e inicializamos la queue
m = QMan(address=('localhost', 60606), authkey=b'cambiame la key')
m.connect()
q = m.get_queue()

# filtro de urls aceptadas
allow = ["youtu.be", "youtube.com", "www.youtube.com"]

## dispatcher y updater del bot de telegram
updater = Updater(env["BOT_KEY"], use_context=True)
dispatcher = updater.dispatcher

## hacemos un chequeo de la url
## y la agregamos a la base de datos
def check_url(username, uid, args):
  ## procesamos la url
  url = args[0]
  u = urlparse(url)
  ## check if the url is what we want
  if u.netloc in allow:
    #get video id (vid)
    if u.path == '/watch':
      vid = u.query.split("v=")[1].split("&")[0]
    else:
      vid = u.path[1:]
    # actualizamos la playlist y notificamos al broker
    with open("site/play.list", "a") as f:
      f.write("%s|%s|%d\n" % (vid, username, uid))
      q.put(time()) # send nudes(?)

## handler de mensajes
# esto es lo que recibe el mensaje y lo despacha a la funcion check_url
@run_async
def add_to_playlist(update, context):
  check_url(update.message.from_user.username, update.message.from_user.id, context.args)

## registramos los comandos que necesitamos
playlist_handler = CommandHandler('playlist', add_to_playlist)
dispatcher.add_handler(playlist_handler)

## arrancamos y no paramos hasta california(?)
updater.start_polling()
updater.idle()