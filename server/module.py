import numpy as np
import sys
from scipy.io.wavfile import read
from scipy.signal import argrelextrema
from math import ceil
import noisereduce as nr
import os
import re

UPLOADS_PATH = os.path.join(os.getcwd(), "uploads")
NOISE_PATH = os.path.join(os.getcwd(), "noise")
np.set_printoptions(threshold=sys.maxsize)

def get_modules(timeStamp):
    modules = []
    for i in range(2):
        modules.append(Module(timeStamp, i))
    return modules

class Module:
    def __init__(self, timeStamp, moduleID):
        self.timeStamp = timeStamp
        self.moduleID = moduleID
        self.channels = [[], [], []]
        self.noisefile = []
        self.frame_total = 1000
        self.chunk_size = 1
        self.num_sounds = 0
        self.zoom = 50
        self.module_events = []

        self.read_files(self.timeStamp)
        self.process_files()

        for channel in self.channels:
            channel = self._smooth(channel, self.chunk_size, self.noisefile)

    def read_files(self, timeStamp, clear_after_read=False):
        file_list = os.listdir(UPLOADS_PATH)
        for file_name in file_list:
            # print(file_list)
            if re.match(r".*\.wav", file_name):
                file_info = file_name.split("-")
                # print(file_info)
                if file_info[2] == str(timeStamp) and file_info[0] == str(self.moduleID):
                    sample_rate, self.channels[int(file_info[1])] = read(
                        os.path.join(UPLOADS_PATH, file_name))
                    if (clear_after_read):
                        os.remove(os.path.join(UPLOADS_PATH, file_name))
                        os.remove(file_info[2])
    
    def process_files(self):
        print(len(self.channels))
        for i, channel in enumerate(self.channels):
            reduced_noise = nr.reduce_noise(audio_clip = channel, noise_clip= self.noisefile, verbose=True)
            try:  # Converts stereo to mono audio
                channel = np.abs(reduced_noise[:, 0]/2) + np.abs(reduced_noise[:, 1]/2)
            except:
                channel = np.abs(reduced_noise[:])
            # Reduces number of samples
            print(i, len(channel))
            try:
                channel = reduced_noise[::len(reduced_noise)//(self.frame_total-1)]
            except:
                pass

    def read_noise(self, clear_after_read = False):
        for file_name in os.listdir(NOISE_PATH):
            if re.match(r".*\.wav", file_name):
                    sample_rate, self.noisefile = read(os.path.join(NOISE_PATH, file_name))
                    if (clear_after_read):
                        os.remove(os.path.join(UPLOADS_PATH, file_name))

    def process_noise(self):
        try:
            self.noisefile = abs(self.noisefile[:,0]/2) + abs(self.noisefile[:,1]/2)
        except:
            self.noisefile = abs(self.noisefile[:])
        self.noisefile = self.noisefile[::len(self.noisefile)//(self.frame_total-1)]


    def find_module_events(self):
        module_threshold = (self._find_event_thresh(self.channels[0]) + self._find_event_thresh(
            self.channels[1]) + self._find_event_thresh(self.channels[2]))/3

        events = [self._find_mic_events(
            channel, module_threshold) for channel in self.channels]

        # TODO: make one function to merge events
        self.module_events = self._merge_events(
            self._merge_events(events[0], events[1]), events[2])

    def _smooth(self, channel, chunk_size, noise_array):
        new_channel = []

        new_len = self.frame_total//chunk_size
        for i in range(new_len + 1):
            total = 0
            for val in channel[i*chunk_size: i*chunk_size + chunk_size]:
                total += val
            total /= chunk_size
            new_channel.append(total)
        return new_channel

    def _return_overlap(self, event_start, event_end, e_list):
        # print("return overlap")
        # print("event_start, event_end: ", event_start, event_end)
        # print("e_list passed:", e_list)
        for k in e_list:
            if (self._overlap(event_start, event_end, k[0], k[1]) and k[2] == False):
                # print("First check")
                # Check if it shares more than 65% of the shorter one
                min_shared = ceil(
                    0.65 * min(k[1] - k[0], event_end-event_start))
                if (min(k[1], event_end) - max(k[0], event_start) >= min_shared):
                    # Return true and the index of k in e_list
                    #print("return_overlap[1] is: ", e_list.index(k))
                    return True, e_list.index(k)
        # Didn't find any overlaps
        return False, 0

    def _merge_events(self, events1, events2):
        e1 = events1[:]
        e2 = events2[:]

        # Add a 3rd element to each event in the arrays to indicate whether or not the event has been considered
        for i in range(len(e1)):
            e1[i].append(False)
        for i in range(len(e2)):
            e2[i].append(False)

        e_merge = []
        # Merge two event lists (e1 and e2)
        for i in range(len(e1)):
            if (e1[i][2] == False):
                # Check if there is a overlapping event in the second list, if not, append the event and mark e1[i] as true
                if (self._return_overlap(e1[i][0], e1[i][1], e2)[0] == False):
                    # print("No conflict")
                    # print("")
                    e_merge.append(e1[i][0:2])
                    e1[i][2] = True
                # If there is an overlapping event
                else:
                    # Perform the merge, append the merged, and mark them both as true
                    merged = []

                    # Mark them both as true
                    e1[i][2] = True

                    # overlapped event:
                    e_overlap = e2[self._return_overlap(e1[i][0], e1[i][1], e2)[1]]
                    # print("return_overlap is: ", return_overlap(e1[i][0], e1[i][1], e2))
                    e2[self._return_overlap(e1[i][0], e1[i][1], e2)[1]][2] = True
                    # print("e_overlap is: ", e_overlap)

                    # Add to the merged event list
                    # print("\nNew merge")
                    merged.append(min(e_overlap[0], e1[i][0]))
                    # print("Min of: ", e_overlap[0], e1[i][0])
                    merged.append(max(e_overlap[1], e1[i][1]))
                    # print("Max of: ", e_overlap[1], e1[i][1])
                    # print("Merged: ", merged)

                    e_merge.append(merged)

        for i in range(len(e2)):
            if (e2[i][2] == False):
                # Check if there is a overlapping event in the second list, if not, append the event and mark e1[i] as true
                if (self._return_overlap(e2[i][0], e2[i][1], e1)[0] == False):
                    # print("No conflict")
                    e_merge.append(e2[i][0:2])
                    e2[i][2] = True
                # If there is an overlapping event
                else:
                    # Perform the merge, append the merged, and mark them both as true
                    merged = []

                    # Mark them both as true
                    e2[i][2] = True

                    # overlapped event:
                    e_overlap = e1[self._return_overlap(e2[i][0], e2[i][1], e1)[1]]
                    e1[self._return_overlap(e2[i][0], e2[i][1], e1)[1]][2] = True

                    # Add to the merged event list
                    merged.append(min(e_overlap[0], e2[i][0]))
                    merged.append(max(e_overlap[1], e2[i][1]))
                    e_merge.append(merged)
        return e_merge

    
    #TODO: This should merged with the above function
    def _overlap(self, a_start, a_end, b_start, b_end):
        if (b_start < a_start and b_end < a_start):
            return False
        if (b_start > a_start and b_end > a_end):
            return False
        return True
    
    def _find_event_thresh(self, arr):
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

    def _find_mic_events(self, sound, threshold):
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

    def determineVolumes(self,start_index, end_index, c1, c2, c3):
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

    def convertToVolumeList(self,event_list, c1, c2, c3):

        volumeList = []

        start_id = 0
        end_id = 0

        for i in range(len(event_list)):
            start_id = event_list[i][0]
            end_id = event_list[i][1]

            volumeList.append(self.determineVolumes(start_id, end_id, c1, c2, c3))

        return volumeList
