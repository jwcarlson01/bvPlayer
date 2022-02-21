# bvPlayer
A borderless video player for python. Comes with a variety of functions such as audio synchronization, FPS adjustment, video scaling, window dragging, and menu options.

Audio synchronization is done through frame skipping and frame delaying. Fps adjustments is done through randomly selecting frames within small chunks. The user is limited to an approximation of their input fps, this is to make the video look smoother.

# Resources
This package was implemented with:
- [opencv](https://pypi.org/project/opencv-python/), for frame loading from a video file
- [Pillow](https://pypi.org/project/Pillow/), for displaying images on tkinter
- [ffpyplayer](https://pypi.org/project/ffpyplayer/), for audio synchronization

# Installation
- Download the repository and run `setup.py`
```
git clone https://github.com/jwcarlson01/bvPlayer.git
python bvPlayer/setup.py
```
- Install from PyPI
```
pip install bvPlayer
```

# Usage
- import the bvPlayer package and class
```
from bvPlayer import bvPlayer
```
- call the class with a filename and optional arguments
```
bvPlayer("file.mp4")
```
The video will play upon the class declaration.
## Optional Arguments
If optional arguments are not specified, the video will default to its orginal fps, (0,0) position on the screen, non-draggable, its original dimensions, and no videoOptions.
<br/><br/>
- fps, to change the display fps to a number less than the file fps
```
fps = float
```
- pos, to change the start-up display location on the screen
```
pos = (int x, int y)
```
- draggable, to make the window draggable
```
draggable = bool
```
- dim, to scale the video output to a desired dimension
```
dim = (int w, int h)
```
- videoOptions, to enable options when right clicking the video, includes quit and restart
```
videoOptions = bool
```

# Example
```
from bvPlayer import bvPlayer

bvPlayer("file.mp4", draggable = True, fps = 28, dim = (854, 480))
```

# Performance
There are two approaches to playing a video on tkinter, either to pregenerate images in a folder and read those images after onto tkinter, or to dynamically load images and display them at the same time.

bvPlayer uses the dynamic approach. bvPlayer uses opencv to load images into temporary files. These temp files are then read by Pillow to be displayed on tkinter. Naturally there is a heavy performance loss using the dynamic approach. bvPlayer uses one thread to read frames, two threads to write frames to temp files, and one thread to display the video and play the audio.

bvPlayer will run a 1080p video on a low end CPU at 20 fps, while using about 60-100% of the CPU. A 480p video will run at 45 fps, using about 40-80% of the CPU; and a 360p video will run at 65 fps, using about 20-60% of the CPU. 

bvPlayer keeps only a small number of frames loaded in RAM, so when running a 1080p video it uses less than 200 MB of RAM.

bvPlayer writes its images to temp files, therefore it uses the disk. Expect at most 5MB/s at 1080p.

# Contact
I'm always open for suggestions. View the [issues page](https://github.com/jwcarlson01/bvPlayer/issues) for issues.

Joshua Carlson - joshuacarlson@cedarville.edu
<br/><br/>
*Readme inspired by [tkvideo](https://github.com/huskeee/tkvideo)*
