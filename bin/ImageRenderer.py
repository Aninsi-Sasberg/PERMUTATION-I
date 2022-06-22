import pyaudio
import numpy as np
import PIL.Image as Image 


# AUDIO VARIABLES
CHUNK = 960
FORMAT = pyaudio.paFloat32
CHANNELS = 1 #Use 1 Channel for Greyscale Image, 3 Channels for RGB Picture. Further Details in the renderImage() Function
RATE = 96000
INDEX = 0   # Use org.py to find out the Indexes of available Audio Devices
RENDERS = 5 #Change Numver of Renders to get multiple Renders of the Audio Stream


#MULTIPLE CHANNEL VALUES ARE INTERLEAVED



p = pyaudio.PyAudio()
                          
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = INDEX,
                frames_per_buffer=CHUNK*CHANNELS)


def convertValue(value):
    #Converting the 32 Bit Float Values of Blackhole Audio Device to 8 Bit unsigned Integers used by PIL to render the Image
    fvalue = np.frombuffer(value, dtype='f')
    out = np.multiply(fvalue, 127)
    return np.add(out, 128).astype(np.uint8)

def getImage():
    #Read the Data of the Audiostream and write it into a 2-3 Dimensional Array depending on the Number of Channels declared above
    Chunksamples = stream.read(CHUNK)
    # print(len(Chunksamples))
    for i in range(CHUNK-1): 
        Chunksamples += stream.read(CHUNK)
        
        print(len(Chunksamples))
        samples = convertValue(Chunksamples)
    return samples #Frame Data    

def renderImage():
    # converting the uint8 Values into Image
    for i in range(RENDERS):
        
        # Choose the following for converting a 3 Channel Audio Stream into RGB Colored Image

        # imgarr = np.reshape(getImage(), (CHUNK,CHUNK,3))
        # img = Image.fromarray(imgarr, 'RGB')

        # Choose the following for converting a 1 Channel Audio Stream into Greyscale Image

        imgarr = np.reshape(getImage(), (CHUNK,CHUNK))
        img = Image.fromarray(imgarr, 'L') 


        img.show()

    
renderImage()
exit()
