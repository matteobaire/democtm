from Tkinter import *
from PIL import Image, ImageTk
from Tkinter import Label
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import os
import sys
import threading
import requests
import scrollingText as st
import psutil
import Queue

message_path = "http://ctm.infora.it/messaggio"
video_path = "/home/pi/Desktop/videos/"


filenames = os.listdir(video_path)


def _quit(event):
    for proc in psutil.process_iter():
        if "omxplayer" in proc.name() or "message_queue" in proc.name():
            proc.kill()
    root.destroy()
    sys.exit(0)
    

def compose_name(directory, video_name):
    return "{}{}".format(directory, video_name)

my_videos = map(lambda x: compose_name(video_path, x), filenames)

def text_loop(queue):
    while True:
        text = None
        req = None
        try:
            req = requests.get(message_path)
        except Exception as e:
            print str(e)
        if req:
            req_content = st.MaskedText(req.content.replace("\r","").replace("\n",""))
            text = st.ScrollingText(str(req_content))
            if not queue.empty():
                queue.get()
            queue.put(text)
        sleep(1)
    
    

def video_loop(master):
    video_count = 0
    width = master.winfo_screenwidth()
    height = master.winfo_screenheight()
    while True:
        
            
        VIDEO_PATH  = Path(my_videos[video_count])

        player = OMXPlayer(VIDEO_PATH)

        player.set_video_pos(width*0.162,height*0.147,width*0.674,height*0.833)

        player.set_aspect_mode('fill')

        sleep(player.duration())


        player.quit()

        video_count = video_count + 1 if video_count < len(my_videos)-1 else 0
            
  
def shift_text(root, message, queue, rot_text):
    delay = 100
    old_text = rot_text
    new_text = old_text
    if not queue.empty():
        new_text = queue.get()
        old_text.replace(new_text)
    old_text.step_left()
    message.set(str(old_text))
    root.after(delay, lambda: shift_text(root, message, queue, old_text))

if __name__ == "__main__":
    message_box = Queue.Queue(maxsize=1)
    message_thread = threading.Thread(target= lambda: text_loop(message_box), name="message_queue")
    message_thread.daemon = True
    message_thread.start()
    try:
        my_message = st.MaskedText("SISTEMA MESSAGGISTICA CTM")
        rot_message = st.ScrollingText(str(my_message))
        root = Tk()
        t = threading.Thread(target=lambda: video_loop(root))
        t.daemon = True
        t.start()
        
        root.attributes("-fullscreen", True)
        root.configure(background='black')
        root.bind("<Escape>", _quit)


        image = Image.open("ctm-500x285.jpg")
        tkpi = ImageTk.PhotoImage(image)
        label_image = Label(root, image=tkpi)
        label_image.place(relx=0.67, rely=0.15, relwidth=0.274, relheight=0.29)

        
        label_image = Label(root)
        label_image.configure(background="white")
        label_image.place(relx=0.67, rely=0.45, relwidth=0.274, relheight=0.29)
        
        videobg = Label(root)
        videobg.configure(background='white')
        videobg.place(relx=0.138, rely=0.099, relwidth=0.509, relheight=0.685)
        
        
        message = StringVar()
        message.set(str(my_message))
        text = Label(root, textvariable=message, font=("Helvetica",40))
        text.configure(background="black", fg="white", anchor='e')
        text.place(relx=0.14, rely=0.9, relwidth=0.51, relheight=0.06)
        shift_text(root, message, message_box, rot_message)
        
        root.mainloop()
        
    except (KeyboardInterrupt, SystemExit):
        print "chiusura"
        sys.exit(0)
