import requests
import json
import os
import subprocess

# url = 'http://87.226.199.130:8890/client/dynamic/recognize'
# wav = open('voice_tmp.wav', 'rb')
#
# res = requests.post(url, data=wav)
#
# wav.close()
#
# print(res)
# print(res.text)
#
# data_answ = json.loads(res.text)
# print(data_answ['hypotheses'][0]['utterance'])


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

    url = 'http://87.226.199.130:8890/client/dynamic/recognize'

    res = requests.post(url, data=data)

    print(res)
    print(res.text)

    data_answ = json.loads(res.text)
    print(data_answ['hypotheses'][0]['utterance'])
    if (
            'hypotheses' in data_answ
            and len(data_answ['hypotheses']) > 0
            and 'utterance' in data_answ['hypotheses'][0]
    ):
        answ = []
        for h in data_answ['hypotheses']:
            if 'utterance' in h:
                answ.append([h['utterance'], 0])
        return answ
    else:
        return 'Ошибка: не удалось распознать голос'


if __name__ == '__main__':
    res = speech2text('../voice_tmp.oga', data=open('voice_tmp.wav', 'rb'))
    print(res)
