from tkinter import *
from . import VideoPlayer

class bvPlayer:
    def __init__(self, file, **kwargs):
        root = Tk()
        player = VideoPlayer(root, file, **kwargs)

        try:
            player.play()
        except KeyboardInterrupt:
            player.kill()
            
        root.mainloop()

bvPlayer('tree480.mp4', fps = 28, pos = (0, 0), draggable = True,
         dim = (1260,720), videoOptions = True)
