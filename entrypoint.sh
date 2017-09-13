#!/bin/sh
PYTHONPATH=$PYTHONPATH:.
python server.py &
huey_consumer -w 4 tasks.huey
