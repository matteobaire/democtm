#!/usr/bin/env python

import os
import shutil
import subprocess
import urllib2
import time
import sys

BASE_URL = "ctm.infora.it"
VIDEOS_URL = "video"

DESTINATION_TMP_DIR = "/tmp/videos"
DESTINATION_DIR = "/home/pi/Desktop/videos"

video_paths ={}

if not os.path.exists(DESTINATION_DIR):
    os.makedirs(DESTINATION_DIR)

WGET_COMMAND = "wget -c -N -P  {} {} --retry-connrefused --waitretry=1 --tries=0 --read-timeout=20 --timeout=900 --continue -t 0"


#funzione print su stessa linea
def print_no_newline(string):
    sys.stdout.write(string)
    sys.stdout.flush()


#  Chiamata del comando wget
def wget(path, url):
    subprocess.call([WGET_COMMAND.format(path, url), ], shell=True)


def copy_to_tmp():
    if os.path.exists(DESTINATION_TMP_DIR):
        shutil.rmtree(DESTINATION_TMP_DIR)
    shutil.copytree(DESTINATION_DIR, DESTINATION_TMP_DIR)


def switch_from_tmp():
    shutil.rmtree(DESTINATION_DIR)
    shutil.move(DESTINATION_DIR, DESTINATION_TMP_DIR)

csvfile = ""
print_no_newline("Checking videos on server")
while csvfile == "":
    try:
        csvfile = urllib2.urlopen("http://{}/{}".format(BASE_URL, VIDEOS_URL))
    except Exception as e:
        print_no_newline(".")
        time.sleep(2)
   
print "Done."
    
csvfile.readline()
video_urls = [line[1:-3] for line in csvfile]
copy_to_tmp()
for video_url in video_urls:
    print video_url
    wget(DESTINATION_TMP_DIR, video_url)

shutil.rmtree(DESTINATION_DIR)
os.makedirs(DESTINATION_DIR)

for video_url in video_urls:
    fname = video_url.split("/")[-1]
    fname = urllib2.unquote(fname)
    print "Copying file", fname
    shutil.move("{}/{}".format(DESTINATION_TMP_DIR, fname), DESTINATION_DIR)
    os.rename("{}/{}".format(DESTINATION_DIR, fname), "{}/{}".format(DESTINATION_DIR, fname.replace(" ", "_")))

files = os.listdir(DESTINATION_DIR)
files = [i for i in files if i.split(".")[1] == "mp4"]
videos = {"{}".format(i): "{}/{}".format(DESTINATION_DIR, j) for i,j in enumerate(files)}

with open("videos.js", "w") as outfile:
    outfile.write("var videosrc = {}".format(videos))

shutil.rmtree(DESTINATION_TMP_DIR)
print "Done."
