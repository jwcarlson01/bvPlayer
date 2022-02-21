import cv2
import random
import time
from decimal import Decimal
from tkinter import *
from ffpyplayer.player import MediaPlayer
from PIL import Image, ImageTk
import tempfile
import threading
import queue
import os
import sys

class VideoPlayer:
    def __init__(self, root, file, **kwargs):
        self.dest = file
        self.cap = cv2.VideoCapture(self.dest)
        
        self.frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.newfps = self.fps
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.root = root
        self.root.overrideredirect(1)
        root.geometry('+0+0')
        self.resize = False

        for k, val in kwargs.items():
            if k == "fps":
                if val > self.fps:
                    print("Error: requested FPS is higher than file FPS")
                    self.root.destroy()
                    return
                self.newfps = val
            elif k == "pos":
                root.geometry("+%d+%d" %val)
            elif k == "draggable" and val == True:
                root.bind('<Button-1>',self.clickPos)
                root.bind('<B1-Motion>', self.dragWin)
                self.clickx = None
                self.clicky = None
            elif k == "dim":
                if (val[0] == self.width and val[1] == self.height):
                    continue
                self.width = val[0]
                self.height = val[1]
                self.resize = True
            elif k == "videoOptions" and val == True:
                root.bind('<Button-3>', self.options)
                
        self.canvas = Canvas(root, width = self.width, height = self.height)
        self.canvas.pack()
                
        self.fr_lock = threading.Lock()
        self.frames_read = queue.Queue()
        self.frame_files = queue.Queue() # list of temp files
        self.frame_times = []

        self.player = MediaPlayer(self.dest)
        self.player.set_pause(True)

        time.sleep(1)

        self.t1 = threading.Thread(target=self.readFrames)
        self.t2 = threading.Thread(target=self.writeFrames)
        self.t3 = threading.Thread(target=self.writeFrames)

        self.t1.start()
        time.sleep(2)
        self.t2.start()
        self.t3.start()
        time.sleep(1)

        self.playVideo()

        self.t1.join()
        self.t2.join()
        self.t3.join()

    def clickPos(self, event):
        time.sleep(.2)
        self.clickx = event.x
        self.clicky = event.y
        
    def dragWin(self,event):
        winx = self.root.winfo_x()
        winy = self.root.winfo_y()

        x = event.x - self.clickx + winx
        y = event.y - self.clicky + winy
        self.root.geometry("+%d+%d" %(x,y))

    def options(self,event):
        def kill():
            os._exit(1)

        def restart():
            os.execl(sys.executable, sys.executable, *sys.argv)
            
        m = Menu(self.root, tearoff = 0)
        m.add_command(label = "restart", command = restart)
        m.add_command(label = "quit", command=kill)
        m.tk_popup(event.x_root, event.y_root)
        
    def randSelect(self):
        frameList = []
        accuracy = 2

        ratio = round(self.newfps/self.fps,accuracy)
        dec_ratio = Decimal(str(ratio))
        self.newfps = ratio*self.fps
        b = (dec_ratio).as_integer_ratio()

        frame_guarantee = b[0]
        frame_chunk = b[1]

        for i in range(1, self.frames, frame_chunk):
            select = range(i,i+frame_chunk-1)
            samp = random.sample(select,frame_guarantee)
            samp.sort()
            frameList.extend(samp)

        return frameList

    def generateFrameTimes(self):
        newFrames = int(self.frames * self.newfps/self.fps)

        targetTime = 1/self.newfps
        times = 0

        for i in range(newFrames):
            self.frame_times.append(times)
            times += targetTime

    def readFrames(self):
        if(self.fps == self.newfps):
            self.generateFrameTimes()
            while(self.cap.isOpened()):

                if(self.frames_read.qsize() > 10):
                    time.sleep(.01)
                    continue
                
                ret, frame = self.cap.read()
                if ret == True:
                    self.frames_read.put(frame)
                else:
                    break
        else:

            select_list = self.randSelect()
            self.generateFrameTimes()

            counter = 0
            walker = 0
            
            while(self.cap.isOpened()):
                if(self.frames_read.qsize() > 10):
                    time.sleep(.01)
                    continue

                counter += 1
                ret, frame = self.cap.read()
                if ret == False:
                    break
                
                if(select_list[walker] == counter):
                    self.frames_read.put(frame)

                    walker += 1
                    
    def writeFrames(self):

        while True:

            if self.frame_files.qsize() > 20:
                time.sleep(.1)
                continue
            
            p = tempfile.NamedTemporaryFile('wb')
            p.name = p.name + '.jpg'
            
            with self.fr_lock:
                if self.frames_read.empty():
                    break
                
                frame = self.frames_read.get()
                self.frame_files.put(p)

            if self.resize == True:
                frame = cv2.resize(frame, (self.width,self.height),
                                    interpolation = cv2.INTER_AREA)
            cv2.imwrite(p.name,frame)

    def playVideo(self):
        counter = 0

        fps = self.newfps # for testing max frame rate
        print(fps)
        targetTime = 1/fps

        img = None
        self.player.set_pause(False)

        # load up the audio
        audio_frame, val = self.player.get_frame()
        while audio_frame == None:
            audio_frame, val = self.player.get_frame()
            
        running_time = time.time()
        while(not self.frame_files.empty()):
            audio_frame, val = self.player.get_frame()

            if(val == 'eof' or len(self.frame_times) == 0):
                break

            if(audio_frame == None):
                continue

            # for any lag due to cpu, especially for dragging
            if(self.frame_files.qsize() < 5):
                time.sleep(.08)
            
            t = self.frame_times.pop(0)
            pop = self.frame_files.get()

            cur_time = time.time() - running_time
            delay = t - cur_time

            # frame skipping
            if (delay < -targetTime):
                continue

            prevIm = img

            # diplay image
            self.canvas.delete("all")

            try:
                load = Image.open(pop.name)
            except:
                continue

            #load.draft("RGB",(2560,1080)) # doesn't do anything?
            render = ImageTk.PhotoImage(load)
            img = Label(image=render)
            img.image = render
            img.place(x=0, y=0)
            load.close()

            self.root.update()
            
            if prevIm != None:
                prevIm.destroy()

            cur_time = time.time() - running_time
            delay = t - cur_time
            
            if (delay > targetTime):
                time.sleep(targetTime)

        self.player.set_pause(True)
        self.root.destroy()
