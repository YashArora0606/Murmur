""" 
Config file with recording settings 

"""

DEVICE = 'pi'
MIC_RATE = 44100
CHUNK = 4096 #Number of samples per buffer
CHANNELS = 1
RECORD_TIME = 10 #Length of each recording in seconds
DEV_INDEXES = [1] #TODO: Find index from pyaudio
OUTPUT_FILENAME = 'output.wav'

