""" 
Config file with recording settings 

"""
UPLOAD_URL = 'https://42d4f998.ngrok.io/listen'

DEVICE = 'pi'
MIC_RATE = 44100
CHUNK = 4096 #Number of samples per buffer
CHANNELS = 1L
RECORD_TIME = 10 #Length of each recording in seconds
DEV_INDEXES = [2,3,4] #TODO: Find index from pyaudio
OUTPUT_FILENAME = 'output.wav'
MODULE_ID = 0
