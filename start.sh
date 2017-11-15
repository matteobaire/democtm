#!/bin/sh

setterm -cursor off

python syncvideos.py
python gui_embedded_queue.py

exit 0