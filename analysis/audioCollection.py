import numpy as np
import sys
from scipy.io.wavfile import read
import os
import re
import matplotlib.pyplot as plt

import analysis as an

np.set_printoptions(threshold=sys.maxsize)
sounds = []
channel1 = []
channel2 = []
channel3 = []
frame_total = 1000

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

    for i in range(len(sound)):
        volume = sound[i][0]
        channel1.append(abs(volume))

        if abs(volume) > current_loudest:
            current_loudest = abs(volume)

# Takes in start and end index, returns list of average volume of each channel during event
def determineVolumes(start_index, end_index):
    volumes = []

    v1 = 0
    v2 = 0
    v3 = 0

    for i in range(start_index, end_index):
        v1 += channel1[i]
        v2 += channel2[i]
        v3 += channel3[i]

    v1 = v1/(end_index - start_index)
    v2 = v2/(end_index - start_index)
    v3 = v3/(end_index - start_index)

    volumes.append(v1)
    volumes.append(v2)
    volumes.append(v3)

    return volumes

# Takes in list of start and end times of events, converts to list of volumes of all 3 channels
def convertToVolumeList(event_list):

    volumeList = [];

    start_id = 0
    end_id = 0

    for i in range(len(event_list)):
        start_id = event_list[i][0]
        end_id = event_list[i][1]

        volumeList.append(determineVolumes(start_id, end_id))

    return volumeList
