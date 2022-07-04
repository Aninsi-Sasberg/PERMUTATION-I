import numpy as np
import pyaudio

class AudioReader():

    def __init__(self,CHUNK,FORMAT,CHANNELS,RATE,INDEX):
        self.CHUNK = CHUNK
        self.Frame = np.zeros((self.CHUNK,self.CHUNK,3),dtype=np.uint8)
        self.partselector = True
        self.renderstart = False
        self.counter = 0
        self.rendering = False
        

        p = pyaudio.PyAudio()

        self.stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = INDEX,
                frames_per_buffer=CHUNK*CHANNELS)    
        
    def convertValue(self, value):
        fvalue = np.frombuffer(value, dtype='f')
        out = np.multiply(fvalue, 127)
        out = np.add(out, 128).astype(np.uint8)
        out = np.reshape(out, (self.CHUNK,3))
        # print(out)
        return out

    def getFrame(self):
        if len(self.Frame) == self.CHUNK:
            self.Framebuffer = self.Frame[:self.CHUNK]
            return self.Frame[:self.CHUNK]
        else:
            return self.Framebuffer
    
    def getPhase1data(self):
        self.data = self.convertValue(self.stream.read(self.CHUNK))
        self.Frame = np.delete(self.Frame, (0), axis=0)
        self.Frame = np.vstack((self.Frame, [self.data]))

    def getPhase2data(self):
        if self.renderstart == True:
            while self.convertValue(self.stream.read(2))[1] == 128:
                self.Frame = np.zeros((self.CHUNK,self.CHUNK,3), dtype = np.uint8)
            self.renderstart = True
        elif self.renderstart == False:

            self.data = self.convertValue(self.stream.read(self.CHUNK))
            self.Frame[self.counter,] = self.data
            self.counter += 1
            if self.counter >= self.CHUNK:
                self.counter = 0

    def updateSelector(self,sel):
        self.partselector = sel
        if not sel:
            self.counter = 0

    def updateRenderState(self,rendering):
        self.rendering = rendering

    def readFrames(self):
        while self.rendering:
            if self.partselector == True:
                self.getPhase1data()
            else:
                self.getPhase2data()