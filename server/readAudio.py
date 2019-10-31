import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time

# %matplotlib tk

CHUNK = 4000
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()

chosen_device_index = -1;
for x in xrange(0, p.get_device_count()):
    info = p.get_device_info_by_index(x)
    #print p.get_device_info_by_index(x)
    if info["name"] == "pulse":
        chosen_device_index = info["index"]
        print "Chosen Index: ", chosen_device_index

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input_device_index = chosen_device_index,
    input = True,
    output = True,
    frames_per_buffer = CHUNK
)

plt.ion()
fig, ax = plt.subplots()

x = np.arange(0, CHUNK)
data = stream.read(CHUNK)
data_int16 = struct.unpack(str(CHUNK) + 'h', data)
line, = ax.plot(x, data_int16)
#ax.set_xlim([xmin, xmax])
ax.set_ylim([-2**15, (2**15)-1])

while True:
    data = struct.unpack(str(CHUNK) + 'h', stream.read(CHUNK))
    print(data)
    # line.set_ydata(data)
    # fig.canvas.draw()
    # fig.canvas.flush_events()
