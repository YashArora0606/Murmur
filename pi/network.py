import os
import sys
import re
from microphone import MicrophoneInterface
import config
import requests

PATH = os.getcwd()
FILE_SUFFIX = r".*\.wav"

file_list = list(filter(lambda file: re.match(FILE_SUFFIX, file),
                        os.listdir('./output')))  # Gets wav files


def update_file_list():
    """
    Updates file_list
    """
    global file_list
    file_list = list(filter(lambda file: re.match(
        FILE_SUFFIX, file), os.listdir('./output')))


def upload_all(clear_after_upload=False):
    """
    Uploads all wav files to server with a POST request
    clear_after_upload: Should delete the wav files after uploading
    """
    global file_list
    for file_name in file_list:
        with open(PATH+"/output/"+file_name, 'rb') as data:
            print("Sending", PATH+"/output/"+file_name)
            file = {'file': data}
            r = requests.post(config.UPLOAD_URL, files=file)
            print(r.status_code)
            if clear_after_upload and os.path.exists(PATH+"/output/"+file_name):
                os.remove(PATH+"/output/"+file_name)


def print_file_list():
    """
    Debugging function
    """
    global file_list
    update_file_list()
    return bool(file_list)


def main():
    update_file_list()
    upload_all()


if __name__ == "__main__":
    main()
