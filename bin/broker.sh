#!/bin/bash
nohup $(which python) broker.py > /dev/null 2>&1 & echo $! > pid/broker.pid