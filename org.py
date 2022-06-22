import pyaudio
from screeninfo import get_monitors

p = pyaudio.PyAudio()

info = p.get_host_api_info_by_index(0)

numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    print(p.get_device_info_by_host_api_device_index(0, i))

for m in get_monitors():
    print(str(m))
