import cv2
import numpy as np

class Renderer():

    def __init__(self,reader,CHUNK,InitialPhaseState):
        self.CHUNK = CHUNK
        self.reader = reader
        self.rendering = True
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

            imgarr = np.reshape(Frame, (self.CHUNK,self.CHUNK,3))

            frame = cv2.resize(imgarr,(1200,1200))

            cv2.imshow('frame', frame)

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
    