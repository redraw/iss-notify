#!/bin/sh
PYTHONPATH=$PYTHONPATH:.
python server.py &
huey_consumer tasks.huey