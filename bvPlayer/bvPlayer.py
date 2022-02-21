from tkinter import *
from . import VideoPlayer

class bvPlayer:
    def __init__(self, file, **kwargs):
        root = Tk()
        player = VideoPlayer.VideoPlayer(root, file, **kwargs)
        root.mainloop()
