import cv2
from cv2 import BORDER_CONSTANT
import numpy as np

class Renderer():

    def __init__(self,reader,CHUNK,height,bordersize,InitialPhaseState):
        self.CHUNK = CHUNK
        self.reader = reader
        self.rendering = True
        self.height = height
        self.bordersize = bordersize
        self.PhaseState = InitialPhaseState
        
    def updateRenderState(self,renderState):
        self.rendering = renderState

    def updatePhaseState(self,PhaseState):
        self.PhaseState = PhaseState

    def getRendering(self):
        return self.rendering

    def renderVideo(self):
        
        while self.rendering:

            Frame = self.reader.getFrame()

            # imgarr = np.reshape(Frame, (self.CHUNK,self.CHUNK,3))

            frame = cv2.resize(Frame,(self.height,self.height))

            frame = cv2.copyMakeBorder(frame, 0,0,self.bordersize,self.bordersize, BORDER_CONSTANT, None,(0,0,0))

            cv2.imshow('frame', frame)

            cv2.namedWindow('frame', cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty('frame',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

            c = cv2.waitKey(10)

            if c & 0xFF == ord('q'):
                    self.rendering = False
                    break
            elif c & 0xFF == ord(' '):
                if self.PhaseState == True:
                    self.PhaseState = False
                    self.reader.updateSelector(False)
                else:
                    self.PhaseState = True
                    self.reader.updateSelector(True)
                    self.reader.renderstart = False
                print("SPACE")
    