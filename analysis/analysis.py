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
frame_total = 1000
chunk_size = 1

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

    sound = sound[::len(sound)//frame_total]
    current_loudest = 0

    for i in range(len(sound)):
        volume = sound[i][0] # ASSUMES A STEREO SOUND FILE --> Remove [0] for mono files
        print(sound[i])
        channel1.append(abs(volume))
        #Thresholding is for sound event determination:
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

def chonk_avg(arr, chunk_size):
    #Produces a new array of the average volume in each chunk of chunk size
    #New array contains (len(arr)//chunk_size) chunks
    chonks = []
    newLen = frame_total//chunk_size
    for i in range(newLen + 1):
        chunksum = 0
        for val in arr[i*chunk_size : i*chunk_size + chunk_size]:
            chunksum += val
        chunksum /= chunk_size
        chonks.append(chunksum)
    return chonks

def drawPlot(channel, plotId):
    plot = plt.figure(plotId)
    plt.plot(range(len(channel)), channel)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.savefig('plot.png')
    return plot



g = drawPlot(channel1, 0)
f = drawPlot(chonk_avg(channel1, 40), 1)
plt.show()

# plt.plot(range(frame_total/chunk_size + 1), channel1)

