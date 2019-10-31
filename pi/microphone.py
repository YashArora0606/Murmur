import time
import pyaudio
import config
import wave

"""
Microphone class to provide an interface for recording sound
"""
class Microphone:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.device_count = p.get_device_count()
        self.devices = [p.get_device_info_by_index(i) for i in range(self.device_count)]
        self.streams = []
        self.frames = []
    
    def print_devices(self):
        for device in self.devices:
            print(device.get('name'))
            
    def start_stream(self):
        for i in range(len(config.DEV_INDEXES)):
            self.streams.append(
                    self.p.open(
                    format = pyaudio.paInt16,
                    rate = config.MIC_RATE,
                    channels = config.CHANNELS,
                    input_device_index = config.DEV_INDEXES,
                    input = True,
                    frames_per_buffer=config.CHUNK)
                )
        
    def close_streams(self):
        for stream in self.streams:
            stream.stop_stream()
            stream.close()
    
    def read_stream(self):
        for i in range(len(self.streams)):
            frames[i] = []
            for i in range((config.MIC_RATE/config.CHUNK)*config.RECORD_TIME):
                frames[i].append(self.streams[i].read(config.CHUNK))

    def write_wav(self):
        for frame in self.frames:
            wavefile = wave.open(str(time.time()) + config.OUTPUT_FILENAME,'wb')
            wavefile.setnchannels(config.CHANNELS)
            wavefile.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wavefile.setframerate(config.MIC_RATE)
            wavefile.writeframes(b''.join(frames))
            wavefile.close()

        
        