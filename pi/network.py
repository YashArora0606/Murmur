import os
import sys
import re
from microphone import MicrophoneInterface
import config
import requests
PATH = os.getcwd()
FILE_SUFFIX = r".*\.wav"

file_list = list(filter(lambda file: re.match(FILE_SUFFIX, file), os.listdir('./output')))

def update_file_list():
    global file_list
    file_list = list(filter(lambda file: re.match(FILE_SUFFIX, file), os.listdir('./output')))

def upload_all(clear_after_upload = False):
    global file_list
    for file_name in file_list:
        with open(PATH+"/output/"+file_name, 'rb') as data:
            print("Sending", PATH+"/output/"+file_name)
            file = {'file':data}
            r = requests.post(config.UPLOAD_URL, files=file)
            print(r.status_code)
            if clear_after_upload and os.path.exists(PATH+"/output/"+file_name):
                os.remove(PATH+"/output/"+file_name)

def main():
    update_file_list()
    upload_all()

if __name__ == "__main__":
    main()


