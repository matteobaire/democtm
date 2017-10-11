#!/usr/bin/env python


import urllib2, os, datetime, subprocess, time, shutil
BASE_URL = "ctm.infora.it"
VIDEOS_URL = "video"


DESTINATION_TMP_DIR = "/tmp/videos"
DESTINATION_DIR = "/home/pi/Desktop/videos"
if not os.path.exists(DESTINATION_DIR):
    os.makedirs(DESTINATION_DIR)


WGET_COMMAND = "wget -c -N -P %s %s"





#Chiamata del comando wget
def wget(path, url):
    subprocess.call([WGET_COMMAND%(path, url),], shell=True)

def copyToTmp():
    if os.path.exists(DESTINATION_TMP_DIR):
        shutil.rmtree(DESTINATION_TMP_DIR)
    shutil.copytree(DESTINATION_DIR, DESTINATION_TMP_DIR)

def switchFromTmp(fname):
    shutil.rmtree(DESTINATION_DIR)	
    shutil.move(DESTINATION_DIR, DESTINATION_TMP_DIR)


csvfile = urllib2.urlopen("http://%s/%s"%(BASE_URL, VIDEOS_URL))
csvfile.readline()
video_urls = [line[1:-3] for  line in csvfile]
copyToTmp()
for video_url in video_urls:
    print video_url
    wget(DESTINATION_TMP_DIR, video_url)


shutil.rmtree(DESTINATION_DIR)
os.makedirs(DESTINATION_DIR)

for video_url in video_urls:
    fname = video_url.split("/")[-1]
    print "Copying file", fname
    shutil.move(DESTINATION_TMP_DIR + "/%s" % fname, DESTINATION_DIR)

shutil.rmtree(DESTINATION_TMP_DIR)
print "Done."

