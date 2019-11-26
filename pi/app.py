from microphone import MicrophoneInterface
import network
import time
import schedule

m = MicrophoneInterface()

def record_and_send():
    print("Recording...")
    m.start_streams(time.strftime("%I%M%S", time.localtime()))
    m.read_streams()
    m.write_wav()
    m.close_streams()
    network.update_file_list()
    network.print_file_list()
    print("Uploading...")
    network.upload_all(clear_after_upload = True)

schedule.every().minute.at(":00").do(record_and_send)

while True:
    schedule.run_pending()
    time.sleep(0.1)
    
