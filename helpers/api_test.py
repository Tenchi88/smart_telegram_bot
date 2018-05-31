import requests
import json
import base64

# python3 manage.py runserver


def send_request(msg):
    url = 'http://127.0.0.1:8000/bot_api/'
    # url = 'http://192.168.1.198:8000/bot_api/'
    # url = 'http://87.226.199.130:8000/bot_api/'
    # wav = open('voice_tmp.wav', 'rb')
    data = {
        'text': msg,
        # 'text': 'найди триллер с Майклом Дугласом',
        'user_id': '123456789',
        'first_name': 'Name',
        'last_name': 'Surname',
        # 'voice': base64.decodebytes(base64.encodebytes(wav.read()))
    }
    # wav.close()
    jsondata = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    res = requests.post(url, headers=headers, json=data)

    print(res)
    data_answ = json.loads(res.text)
    print(data_answ['answer.text'])
    print('Действие:', data_answ['answer.command'])


if __name__ == '__main__':
    reqs = ['привет', 'да', 'нет', 'телефон 7777777']
    for r in reqs:
        send_request(r)
