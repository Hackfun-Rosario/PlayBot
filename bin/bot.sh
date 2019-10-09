#!/bin/bash
nohup $(which python) bot.py > /dev/null 2>&1 & echo $! > pid/bot.pid
