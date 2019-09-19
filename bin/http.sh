#!/bin/bash
gunicorn --bind 127.0.0.1:8000 --daemon --pid ./pid/http.pid --workers 4 wsgi
