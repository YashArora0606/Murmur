import numpy as np
import sys
from scipy.io.wavfile import read
import os
import re
import matplotlib.pyplot as plt

# PATH = os.cwd()
# OUTPUT_DIR = "/pi/output/"

# numpy list

np.set_printoptions(threshold=sys.maxsize)
sounds = []
channel1 = []
increment_list = []
frame_rate = 1000

for i in range(frame_rate+1):
    increment_list.append(i)


file_list = os.listdir(".")
for file_name in file_list:
    if re.match(".*\.wav", file_name):
        sample_rate, data = read(file_name) # assuming sample rates are the same
        sounds.append(data)

for (index, sound) in enumerate(sounds):
    try:
        sound = sounds[:,0] + sounds[:,1]
    except:
        pass

    sound = sound[::len(sound)/frame_rate]
    current_loudest = 0;

    for i in range(len(sound)):
        volume = sound[i][0]
        channel1.append(abs(volume))
        if abs(volume) > current_loudest:
            current_loudest = abs(volume)

num_sounds = 0
threshold = current_loudest/4

for i in range(len(channel1)):
    if abs(channel1[i]) >= threshold:
        # find when the sound goes back below the threshold
        # increment the number of num_sounds
        # continue from the new position of i, which is when the sound has gone below the threshold
        pass


print(num_sounds)

def summarize(arr, chunk_size):
    pass

plt.plot(increment_list, channel1)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.savefig('plot.png')

plt.show()
