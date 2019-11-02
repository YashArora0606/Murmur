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
channel2 = []
channel3 = []
frame_total = 1000
chunk_size = 1

file_list = os.listdir(".")
for file_name in file_list:
    if re.match(".*\.wav", file_name):
        sample_rate, data = read(file_name) # assuming sample rates are the same
        sounds.append(data)

current_loudest = 0

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

num_sounds = 0

#Smooth function implemented using NUMPY library. Not currently in use (Nov 1)
def smooth(x, window_len=15):
    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    w=np.ones(window_len,'d')
    y=np.convolve(w/w.sum(),s,mode='valid')
    print(len(y))
    return y

#Smoothing function that is currently in use
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

#Finds events for a single module. Takes in 3 sound arrays - one from each microphone and a minimum volume threshold for defining events
#Returns an array of (start index, duration) of sound events with start and end measured in indices of the sound array
def find_module_events(s1, s2, s3):
    #Don't let a sound event endure for too long - set a max
    module_thresh = (find_event_thresh(s1) + find_event_thresh(s2) +find_event_thresh(s3))/3
    e1 = find_mic_events(s1, module_thresh)
    e2 = find_mic_events(s2, module_thresh)
    e3 = find_mic_events(s3, module_thresh)

    

    pass

#HELPER FUNCTION for find module events
#Very primitive threshold definition
#Takes the SUMMARIZED/chunked sound array and returns the threshold value
def find_event_thresh(arr):
    max_vol = 0
    for vol in arr:
        if vol > max_vol:
            max_vol = vol
    return max_vol/3

#HELPER FUNCTION for find module events
#Find the sound events for one mic given a threshold and sound array
#Same return format as find_module_events but for one mic
def find_mic_events(sound, threshold):
    event_on = False
    events = []
    print(threshold)
    for i in range(len(sound)):
        vol = sound[i]
        if (vol > threshold and not event_on):
            event_start = i
            event_on = True
        if (vol < threshold and event_on):
            event_end = i
            event_on = False
            events.append((event_start, event_end))
   #ADD FEATURE: Coallesce short events that are very close together
    return events

#Takes a 1D array of volume values over time, and determines an event volume threshold
#Returns int value

#Takes in a 1D array and plots y = val, x = index. PlotID determines the order in which the plots are displayed.
#Plot ID is mANDATORY to display properly. Set each plot ID as one greater than the previous.
def drawPlot(channel, plotId):
    plot = plt.figure(plotId)
    plt.plot(range(len(channel)), channel)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.savefig('plot.png')
    return plot

#Create plot of original sound file
g = drawPlot(channel1, 0)

smoothChannel = chonk_avg(channel1, 20)
threshold = find_event_thresh(smoothChannel)

#f = Plot of smoothed sound file
f = drawPlot(smoothChannel, 1)
plt.show()

e1 = find_mic_events(smoothChannel, threshold)
print(e1)

# plt.plot(range(frame_total/chunk_size + 1), channel1)
