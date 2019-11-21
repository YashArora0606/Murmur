import time
import pyaudio
import config
import wave

"""
Microphone class to provide an interface for recording sound
"""
class MicrophoneInterface:
    def __init__(self, indexes=[]):
        self.p = pyaudio.PyAudio()
        self.device_count = self.p.get_device_count()
        self.devices = [self.p.get_device_info_by_index(i) for i in range(self.device_count)]
        self.streams = []
        self.frames = {}
    """
    Shows devices that are recognized currently
    """
    def print_devices(self):
        for device in self.devices:
            print(device.get('name'))
            print(device)
    """
    Starts recording on all audio devices
    """
    def start_streams(self):
        for i in range(len(config.DEV_INDEXES)):
            self.streams.append(
                    self.p.open(
                    format = pyaudio.paInt16,
                    rate = config.MIC_RATE,
                    channels = config.CHANNELS,
                    input_device_index = config.DEV_INDEXES[i],
                    input = True,
                    frames_per_buffer=config.CHUNK)
                )
            self.frames[i] = []

    def close_streams(self):
        for stream in self.streams:
            stream.stop_stream()
            stream.close()
	    self.streams = []
    """
    Reads data in stream
    """
    def read_streams(self):
        for i in range((config.MIC_RATE/config.CHUNK)*config.RECORD_TIME):
            for j in range(len(self.streams)):
                self.frames[j].append(self.streams[j].read(config.CHUNK, exception_on_overflow=False))
    """
    Creates wav files
    """
    def write_wav(self):
	current_time = time.strftime("%I%M%S", time.localtime())
        for i in range(len(self.frames)):
	    print(i)
            wavefile = wave.open("./output/" + str(config.MODULE_ID) + "-" + str(i) + "-" + current_time + ".wav",'wb')
            wavefile.setnchannels(config.CHANNELS)
            wavefile.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wavefile.setframerate(config.MIC_RATE)
            wavefile.writeframes(b''.join(self.frames[i]))
            wavefile.close()
        self.frames = {}

def main():
    m = MicrophoneInterface()
    print("start script")
    m.print_devices()
    m.start_streams()
    m.read_streams()
    m.write_wav()
    m.close_streams()
    print("done")
    
    
if __name__ == '__main__':
    main()
   
