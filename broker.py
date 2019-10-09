#!/usr/bin/env python3

## descripcion
# el broker comunica ambos procesos (bot y server wsgi) para avisar cuando se actualiza la playlist

from multiprocessing.managers import BaseManager
import queue

# creamos la cola de mensajes para los clientes
q = queue.Queue()

# creamos la clase
class QMan(BaseManager):
  pass

# registramos el metodo 'get_queue' para compartir la cola con los clientes
QMan.register('get_queue', callable=lambda:q)

## brrrum brrrum! corremos el server
m = QMan(address=('localhost', 60606), authkey=b'cambiame la key')
s = m.get_server()
s.serve_forever()