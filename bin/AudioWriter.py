from PIL import Image
import numpy as np
from scipy.io.wavfile import write

imgpath = "res/pipe1.png"

# with Image.open(imgpath).convert('L') as img:
#     imgarr = np.array(img)
imgarr = np.asarray(Image.open(imgpath).convert('L'))
imgarr = imgarr.flatten()
print(len(imgarr))

scaled = (imgarr/255).astype(np.float32)
# print(scaled)
# print(len(imgarr))
write('pipe1.wav', 96000, scaled)
