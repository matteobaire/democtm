#!/bin/sh

# get rid of the cursor so we don't see it when videos are running
setterm -cursor off

/usr/bin/chromium-browser --kiosk videos.html
