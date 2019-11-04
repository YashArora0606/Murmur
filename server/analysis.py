import numpy as np
import sys
from scipy.io.wavfile import read
from scipy.signal import argrelextrema
from math import ceil
import os
import re
import matplotlib.pyplot as plt

# PATH = os.cwd()
# OUTPUT_DIR = "/pi/output/"

# numpy list

np.set_printoptions(threshold=sys.maxsize)
channel1 = []
channel2 = []
channel3 = []
frame_total = 1000
chunk_size = 1
num_sounds = 0

UPLOADS_PATH = os.path.join(os.getcwd(),"uploads")

def read_files(clear_after_read = False):
    global channel1, channel2, channel3
    file_list = os.listdir(UPLOADS_PATH)
    for file_name in file_list:
        if re.match(r".*\.wav", file_name):
            file_info = file_name.split("-")
            if (file_info[1] == '0'):
                sample_rate, channel1 = read(os.path.join(UPLOADS_PATH, file_name))
                if (clear_after_read):
                    os.remove(os.path.join(UPLOADS_PATH, file_name))
            elif (file_info[1] == '1'):
                sample_rate, channel2 = read(os.path.join(UPLOADS_PATH, file_name))
                if (clear_after_read):
                    os.remove(os.path.join(UPLOADS_PATH, file_name))
            elif (file_info[1] == '2'):
                sample_rate, channel3 = read(os.path.join(UPLOADS_PATH, file_name)) # assuming sample rates are the same
                if (clear_after_read):
                    os.remove(os.path.join(UPLOADS_PATH, file_name))

def process_files():
    global channel1, channel2, channel3, frame_total
    try:
        channel1 = abs(channel1[:,0]/2) + abs(channel1[:,1]/2)
        channel2 = abs(channel2[:,0]/2) + abs(channel2[:,1]/2)
        channel3 = abs(channel3[:,0]/2) + abs(channel3[:,1]/2)
    except:
        pass
    channel1 = channel1[::len(channel1)//(frame_total-1)]
    channel2 = channel2[::len(channel2)//(frame_total-1)]
    channel3 = channel3[::len(channel3)//(frame_total-1)]

#Smooth function implemented using NUMPY library. Not currently in use (Nov 1)
def smooth(x, window_len = 15):
    s = np.r_[x[window_len-1:0:-1], x, x[-2:-window_len-1:-1]]
    #print(len(s))
    w = np.ones(window_len,'d')
    y = np.convolve(w / w.sum(), s, mode = 'valid')
    # print(len(y))
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
#Returns an array of (start index, stop index) of sound events with start and end measured in indices of the sound array
def find_module_events(s1, s2, s3):
    #Don't let a sound event endure for too long - set a max
    module_thresh = (find_event_thresh(s1) + find_event_thresh(s2) +find_event_thresh(s3))/3

    e1 = find_mic_events(s1, module_thresh)
    print("             e1 is:", e1)
    e2 = find_mic_events(s2, module_thresh)
    print("             e2 is:", e2)
    e3 = find_mic_events(s3, module_thresh)

    print("Merge of e1 and e2:", e_merge_two(e1, e2))

    #Final module list
    e_module = e_merge_two(e_merge_two(e1, e2), e3)

    #Chop off the last element from all e_module list elemements
    return e_module

def e_merge_two(events1, events2):
    e1 = events1[:]
    e2 = events2[:]

    #Add a 3rd element to each event in the arrays to indicate whether or not the event has been considered
    for i in range(len(e1)):
        e1[i].append(False)
    for i in range(len(e2)):
        e2[i].append(False)

    e_merge = []
     #Merge two event lists (e1 and e2)
    for i in  range(len(e1)):
        if (e1[i][2] == False):
        #Check if there is a overlapping event in the second list, if not, append the event and mark e1[i] as true
            if (return_overlap(e1[i][0], e1[i][1], e2)[0] == False):
                # print("No conflict")
                # print("")
                e_merge.append(e1[i][0:2])
                e1[i][2] = True
            #If there is an overlapping event
            else:
                #Perform the merge, append the merged, and mark them both as true
                merged = []

                #Mark them both as true
                e1[i][2] = True

                #overlapped event:
                e_overlap = e2[return_overlap(e1[i][0], e1[i][1], e2)[1]]
                # print("return_overlap is: ", return_overlap(e1[i][0], e1[i][1], e2))
                e2[return_overlap(e1[i][0], e1[i][1], e2)[1]][2] = True
                # print("e_overlap is: ", e_overlap)

                #Add to the merged event list
                # print("\nNew merge")
                merged.append(min(e_overlap[0], e1[i][0]))
                # print("Min of: ", e_overlap[0], e1[i][0])
                merged.append(max(e_overlap[1], e1[i][1]))
                # print("Max of: ", e_overlap[1], e1[i][1])
                # print("Merged: ", merged)

                e_merge.append(merged)

    for i in  range(len(e2)):
        if (e2[i][2] == False):
        #Check if there is a overlapping event in the second list, if not, append the event and mark e1[i] as true
            if (return_overlap(e2[i][0], e2[i][1], e1)[0] == False):
                # print("No conflict")
                e_merge.append(e2[i][0:2])
                e2[i][2] = True
            #If there is an overlapping event
            else:
                #Perform the merge, append the merged, and mark them both as true
                merged = []

                #Mark them both as true
                e2[i][2] = True

                #overlapped event:
                e_overlap = e1[return_overlap(e2[i][0], e2[i][1], e1)[1]]
                e1[return_overlap(e2[i][0], e2[i][1], e1)[1]][2] = True

                #Add to the merged event list
                merged.append(min(e_overlap[0], e2[i][0]))
                merged.append(max(e_overlap[1], e2[i][1]))
                e_merge.append(merged)
    return e_merge


#Return an overlap if it shares more than 65% of the shorter duration. If more than one exists, returns earlier one.
def return_overlap(event_start,event_end,e_list):
    # print("return overlap")
    # print("event_start, event_end: ", event_start, event_end)
    # print("e_list passed:", e_list)
    for k in e_list:
        if (overlap(event_start, event_end, k[0], k[1]) and k[2] == False):
            # print("First check")
            #Check if it shares more than 65% of the shorter one
            min_shared = ceil (0.65 * min(k[1] - k[0], event_end-event_start))
            if (min(k[1], event_end) - max(k[0], event_start) >= min_shared):
                #Return true and the index of k in e_list
                #print("return_overlap[1] is: ", e_list.index(k))
                return True, e_list.index(k)
    #Didn't find any overlaps
    return False, 0

def overlap(a_start, a_end, b_start, b_end):
    if (b_start < a_start and b_end < a_start):
        return False
    if (b_start > a_start and b_end > a_end):
        return False
    return True

# HELPER FUNCTION for find module events
# Takes the SUMMARIZED/chunked sound array and returns the threshold value
# Takes the sum of the localMinima and localMaxima  and divides by the number of these local extrema
def find_event_thresh(arr):

    # initializes a new numpy array that has the same value as the one passed in
    numpy_arr = np.array(arr)

    # Creates an array of the indices of the local extrema
    minima = argrelextrema(numpy_arr, np.less_equal)[0]
    maxima = argrelextrema(numpy_arr, np.greater_equal)[0]

    # Adds all values of local minimums
    sum_local_min = 0
    for numLocalMin in np.nditer(minima):
        sum_local_min += numpy_arr[numLocalMin]

    # Adds all values of local maximums
    sum_local_max = 0
    for numLocalMax in np.nditer(maxima):
        sum_local_max += numpy_arr[numLocalMax]

    # Calculates threshold value
    threshold_vol = (sum_local_min + sum_local_max) / (len(maxima) + len(minima))
    # print(threshold_vol)

    return threshold_vol

#HELPER FUNCTION for find module events
#Find the sound events for one mic given a threshold and sound array
#Same return format as find_module_events but for one mic
def find_mic_events(sound, threshold):
    event_on = False
    events = []
    # print(threshold)
    for i in range(len(sound)):
        vol = sound[i]
        if (vol > threshold and not event_on):
            event_start = i
            event_on = True
        if (vol < threshold and event_on):
            event_end = i
            event_on = False
            events.append([event_start, event_end])
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

def determineVolumes(start_index, end_index, c1, c2, c3):
    volumes = []

    v1 = 0
    v2 = 0
    v3 = 0

    for i in range(start_index, end_index):
        v1 += c1[i]
        v2 += c2[i]
        v3 += c3[i]

    v1 = v1/(end_index - start_index)
    v2 = v2/(end_index - start_index)
    v3 = v3/(end_index - start_index)

    volumes.append(v1)
    volumes.append(v2)
    volumes.append(v3)

    return volumes

def convertToVolumeList(event_list, c1, c2, c3):

    volumeList = []

    start_id = 0
    end_id = 0

    for i in range(len(event_list)):
        start_id = event_list[i][0]
        end_id = event_list[i][1]

        volumeList.append(determineVolumes(start_id, end_id, c1, c2, c3))

    return volumeList

#Create plot of original sound file
#g = drawPlot(channel1, 0)

#smoothChannel = chonk_avg(channel1, 20)
#threshold = find_event_thresh(smoothChannel)

#f = Plot of smoothed sound file
#f = drawPlot(smoothChannel, 1)

#Uncomment this to show the plots:
#plt.show()
#plt.plot(range(frame_total/chunk_size + 1), channel1)


#print(find_mic_events(channel1, threshold))
#print("\n")
#print(find_module_events(channel1, channel1, channel1))

def main():
    read_files()
    process_files()

    smooth1 = chonk_avg(channel1, 25)
    smooth2 = chonk_avg(channel2, 25)
    smooth3 = chonk_avg(channel3, 25)

    drawPlot(smooth1, 1)
    plt.axhline(y=find_event_thresh(smooth1), color='r', linestyle='-')
    plt.xticks(range(0, len(smooth1), 1))

    drawPlot(smooth2, 2)
    drawPlot(smooth3, 3)

    # print(find_module_events(smooth1, smooth2, smooth3))
    # volumes_list = convertToVolumeList(find_module_events(smooth1, smooth2, smooth3), smooth1, smooth2, smooth3)
    # print(volumes_list)

    plt.show()

    find_module_events(smooth1 ,smooth2, smooth3)


if __name__ == "__main__":
    main()
