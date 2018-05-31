import requests
from uuid import uuid1
import os
import xml.etree.ElementTree as ET
import subprocess


def speech2text(speech_file=None, data=None):
    if data is None:
        dest_filename = 'voice_tmp.wav'
        if os.path.exists(dest_filename):
            os.remove(dest_filename)

        process = subprocess.run(
            ['ffmpeg', '-loglevel', 'panic', '-i', speech_file, dest_filename]
        )
        if process.returncode != 0:
            return 'Невозможно преобразовать файл {} в .wav'.format(speech_file)
        data = open('voice_tmp.wav', 'rb').read()

    key = '01b26637-c5dc-402f-bbfc-3329322cc0a7'
    uuid = uuid1()
    url = 'https://asr.yandex.net/asr_xml?key=' + key + '&uuid=' + uuid.hex \
          + '&topic=queries&lang=ru-RU'
    headers = {"Content-Type": 'audio/x-wav'}
    # print(data)
    # print(url)

    res = requests.post(url, headers=headers, data=data)
    # print(res)
    # print(res.text)

    root = ET.fromstring(res.text)
    return [(x.text, x.attrib['confidence']) for x in root.findall('variant')]


if __name__ == '__main__':
    res = speech2text('../voice_tmp.oga')
    print(res)
