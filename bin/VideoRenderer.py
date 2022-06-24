
import pyaudio
import numpy as np
import PIL.Image as Image 
import threading
import cv2
import time
import screeninfo

# AUDIO VARIABLES
CHUNK = 960 
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 96000
INDEX = 0
RENDERS = 1
MONITOR = 1

#MULTIPLE CHANNEL VALUES ARE INTERLEAVED

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = INDEX,
                frames_per_buffer=CHUNK*CHANNELS)

def convertValue(value):
    fvalue = np.frombuffer(value, dtype='f')
    out = np.multiply(fvalue, 127)
    out = np.add(out, 128).astype(np.uint8)
    # print(out)
    return out

def getRow():
    Chunksamples = stream.read(CHUNK)  
    samples = convertValue(Chunksamples)
    return samples


def renderVideo(readthing):
    
    while rendering:
        imgarr = readthing.getFrame()
        # imgarr = np.reshape(Frame, (CHUNK,CHUNK))
        # i = imgarr.flatten()
        # print(len(i))
        frame = cv2.resize(imgarr,(1200,1200))
        
        cv2.imshow('frame', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            print(frame)
            break
        

class AudioReader():

    def __init__(self):
        self.Frame = np.zeros((CHUNK,CHUNK),dtype=np.uint8)
    def readFrames(self):
        while rendering:
            
            self.data = convertValue(stream.read(CHUNK))
            self.Frame = np.delete(self.Frame, (0), axis=0)
            self.Frame = np.vstack([self.Frame, self.data])
           
            
    def getFrame(self):
        if len(self.Frame) == CHUNK:
            return self.Frame[:CHUNK]
        else:
            time.sleep(0.001)
            return self.Frame[:CHUNK]
       

global rendering

screen = screeninfo.get_monitors()[MONITOR]
width, height = screen.width, screen.height


rendering = True
reader = AudioReader()
x = threading.Thread(target=reader.readFrames)
x.start()


# window_name = 'projector'
# cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

renderVideo(reader)
rendering = False
cv2.destroyAllWindows()



exit()
