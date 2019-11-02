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
        channel1.append(abs(volume))
        #Thresholding is for sound event determination:
        if abs(volume) > current_loudest:
            current_loudest = abs(volume)

num_sounds = 0

#Very primitive threshold definition
threshold = current_loudest/3

#Finds events for a single module. Takes in 3 event arrays - one from each microphone and a minimum volume threshold for defining events
#Returns an array of (start index, duration) of sound events with start and duration measured in indices of the sound array
def find_module_events(e1, e2, e3): 
    #Don't let a sound event endure for too long - set a max


    pass

#Find the sound events for one mic
#Same return format as find_module_events
def find_mic_events(sound, threshold):
    event_on = False
    events = []
    for vol in (sound):
        if (vol > threshold and not event_on):
            event_start = vol
            event_on = True
        if (vol < threshold and event_on):
            event_dur = vol - event_start
            event_on = False
            events.append([event_start, event_dur])
   #ADD FEATURE: Coallesce short events that are very close together
    return events

#Takes a 1D array of volume values over time, and determines an event volume threshold
#Returns int value

#Smooth function implemented using NUMPY library. Not currently in use (Nov 1)
def smooth(x, window_len=15):
    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    w=np.ones(window_len,'d')
    y=np.convolve(w/w.sum(),s,mode='valid')
    print(len(y))
    return y

def chonk_avg(arr, chunk_size):
    #Produces a new array of the average value in each chunk of  chunk_size
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

#Takes in a 1D array and plots y = val, x = index. PlotID determines the order in which the plots are displayed.
#Plot ID is mANDATORY to display properly. Set each plot ID as one greater than the previous. 
def drawPlot(channel, plotId):
    plot = plt.figure(plotId)
    plt.plot(range(len(channel)), channel)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.savefig('plot.png')
    return plot


g = drawPlot(channel1, 0)
f = drawPlot(chonk_avg(channel1, 20), 1)
x = drawPlot(smooth(channel1), 2)
plt.show()

# plt.plot(range(frame_total/chunk_size + 1), channel1)

