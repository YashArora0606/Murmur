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
        volume = sound[i][0] # ASSUMES A STEREO SOUND FILE --> Remove [0] for mono files
        channel1.append(abs(volume))
        #Thresholding is for sound event determination:
        if abs(volume) > current_loudest:
            current_loudest = abs(volume)

# Takes in list of start and end times of events, converts to list of volumes of all 3 channels
def convertToVolumeList(event_list):

    volumeList = [];

    start_id = 0
    end_id = 0

    for i in range(len(event_list)):
        start_id = event_list[i][0]
        end_id = event_list[i][1]

        volumeList.append(an.determineVolumes(start_id, end_id))

    return volumeList






# g = drawPlot(channel1, 0)
# f = drawPlot(chonk_avg(channel1, 20), 1)



# f = an.drawPlot(channel1, 1)
# x = an.drawPlot(an.smooth(channel1), 2)
# plt.show()
