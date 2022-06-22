
import pyaudio
import numpy as np
import threading
import cv2
import time

# AUDIO VARIABLES
CHUNK = 480
FORMAT = pyaudio.paFloat32
CHANNELS = 3
RATE = 48000
INDEX = 0
RENDERS = 1

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
    out = np.reshape(out, (CHUNK,3))
    # print(out)
    return out


def renderVideo(readthing):
    
    while rendering:
        Frame = readthing.getFrame()
        imgarr = np.reshape(Frame, (CHUNK,CHUNK,3))
        frame = cv2.resize(imgarr,(1200,1200))
        cv2.imshow('frame', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        

class AudioReader():

    def __init__(self):
        self.Frame = np.zeros((CHUNK,CHUNK,3),dtype=np.uint8)
    def readFrames(self):
        while rendering:
            
            self.data = convertValue(stream.read(CHUNK))
            print(self.data)
            self.Frame = np.delete(self.Frame, (0), axis=0)
            self.Frame = np.vstack((self.Frame, [self.data]))
           
            
    def getFrame(self):
        if len(self.Frame) == CHUNK:
            return self.Frame[:CHUNK]
        else:
            time.sleep(0.001)
            return self.Frame[:CHUNK]
       

global rendering
rendering = True

reader = AudioReader()
x = threading.Thread(target=reader.readFrames)
x.start()

renderVideo(reader)
cv2.destroyAllWindows()


exit()
