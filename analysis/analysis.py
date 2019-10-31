import numpy as np
from scipy.io import wavfile
import os
import re

PATH = os.path.abspath('..')
OUTPUT_DIR = "/pi/output"
WAV_SUFFIX = re.compile("*.wav$")

sounds = []

file_list = os.listdir(PATH+OUTPUT_DIR)
for file_name in file_list:
    if re.match(WAV_SUFFIX, file_name):
        sample_rate, data = wavfile.read(PATH+OUTPUT_DIR+file_name) # assuming sample rates are the same
        sounds.append(data)

for (index, sound) in enumerate(sounds):
    sound = sound[:,0] + sound[:,1]
    sound = sounds[::len(sound)/10]
    for i in len(sound):
        print(sound[i])    

