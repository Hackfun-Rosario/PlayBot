#!/bin/bash
nohup $(which python) wsgi.py > /dev/null 2>&1 & echo $! > pid/http.pid
