from cv2 import BORDER_CONSTANT
import pyaudio
import numpy as np
import threading
import cv2
import time
import screeninfo

# VARIABLES
CHUNK = 960
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 96000
INDEX = 1
MONITOR = 0




def convertValue(value):

    fvalue = np.frombuffer(value, dtype='f')
    out = np.multiply(fvalue, 127)
    out = np.add(out, 128).astype(np.uint8)
    return out


def renderVideo(readthing,partselector):

    while rendering:

        imgarr = readthing.getFrame()
       
        frame = cv2.resize(imgarr,(height,height))
        
        frame = cv2.copyMakeBorder(frame, 0,0,bordersize,bordersize, BORDER_CONSTANT, None,(0,0,0))

        cv2.imshow('window', frame)

        c = cv2.waitKey(10)

        if c & 0xFF == ord('q'):
            print(frame)
            break
        elif c & 0xFF == ord(' '):
            if partselector == True:
                partselector = False
                reader.updateSelector(False)
            else:
                partselector = True
                reader.updateSelector(True)
            print("SPACE")
            print(partselector)

        

class AudioReader():

    def __init__(self,partselector):

        self.Frame = np.zeros((CHUNK,CHUNK),dtype=np.uint8)
        self.partselector = partselector
        self.counter = 0




    def readFrames(self):
        
        while rendering:
            print(self.partselector)

            if self.partselector == True:
                self.getPhase1data()

            else:
                self.getPhase2data()
                # if convertValue(stream.read(1)) == 0:
                #     pass
                # else:
                    


    def getFrame(self):

        if len(self.Frame) == CHUNK:

            self.Framebuffer = self.Frame[:CHUNK]
            return self.Frame[:CHUNK]

        else:

            return self.Framebuffer
    
    def getPhase1data(self):
        self.data = convertValue(stream.read(CHUNK))
        self.Frame = np.delete(self.Frame, (0), axis=0)
        self.Frame = np.vstack([self.Frame, self.data])

    def getPhase2data(self):
        self.data = convertValue(stream.read(CHUNK))
        self.Frame[self.counter,] = self.data
        self.counter += 1
        if self.counter >= CHUNK:
            self.counter = 0

    def updateSelector(self,sel):
        self.partselector = sel
        if not sel:
            self.counter = 0
       

global rendering, bordersize, width, height, window

screen = screeninfo.get_monitors()[MONITOR]

width, height = screen.width, screen.height
bordersize = int((width-height)/2)
partselector = True
reader = AudioReader(partselector)

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = INDEX,
                frames_per_buffer=CHUNK*CHANNELS)

rendering = True



x = threading.Thread(target=reader.readFrames)
x.start()

renderVideo(reader,partselector)

rendering = False
cv2.destroyAllWindows()
exit()