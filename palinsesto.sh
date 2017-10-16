#!/bin/sh

# get rid of the cursor so we don't see it when videos are running
setterm -cursor off

/usr/bin/chromium-browser --disable-web-security --user-data-dir --kiosk videos.html
