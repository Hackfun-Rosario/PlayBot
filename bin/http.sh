#!/bin/bash
#gunicorn --bind 127.0.0.1:8000 --daemon --pid ./pid/http.pid --workers 4 wsgi
nohup $(which python) wsgi.py > /dev/null 2>&1 & echo $! > pid/http.pid
