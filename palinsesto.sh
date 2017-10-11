#!/bin/sh

# set here the path to the directory containing your videos
VIDEOPATH="/home/pi/Desktop/videos/" 

# now for our infinite loop!
#while true; do
        if ps ax | grep -v grep | grep $SERVICE > /dev/null
        then
        sleep 1;
else
        for entry in $VIDEOPATH/*
        do
                clear
 
                # -r for stretched over the entire screen
                /usr/bin/chromium-browser  --args --disable-web-security --user-data-dir --disable-infobars --kiosk $entry > /dev/null
		sleep exitfool -S -n $entry | grep ^Duration
	done
fi
#done



