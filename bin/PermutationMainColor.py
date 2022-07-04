
import pyaudio
import numpy as np
import threading
import cv2
import screeninfo
from AudioReader import AudioReader
from Renderer import Renderer

# AUDIO VARIABLES
CHUNK = 480
FORMAT = pyaudio.paFloat32
CHANNELS = 3
RATE = 48000
INDEX = 0
MONITOR = 0


screen = screeninfo.get_monitors()[MONITOR]
width, height = screen.width, screen.height
bordersize = int((width-height)/2)

initialPhaseState = True

reader = AudioReader(CHUNK,FORMAT,CHANNELS,RATE,INDEX)
renderer = Renderer(reader, CHUNK,initialPhaseState)
                
rendering = True
reader.updateRenderState(rendering)

a = threading.Thread(target=reader.readFrames)
a.start()

v = threading.Thread(target=renderer.renderVideo())
v.start()

while rendering:
    rendering = renderer.getRendering()



reader.updateRenderState(rendering)

cv2.destroyAllWindows()


exit()
