import requests
import json
import base64

base_url = 'https://cp.speechpro.com/vkasr/rest'
url = base_url + '/session'
data = {
  "username": "rt@rt.ru",
  "password": "1q2w#E",
  "domain_id": 284
}
jsondata = json.dumps(data)
headers = {'Content-Type': 'application/json'}
res = requests.post(url, headers=headers, data=jsondata)

print(res)
print(res.text)

session_dict = dict(eval(res.text))
print(session_dict['session_id'])
session_id = session_dict['session_id']

url = base_url + '/v1/packages/available'
headers = {'X-Session-Id': session_id}
res = requests.get(url, headers=headers)

print(res)
print(res.text)


url = base_url + '/v1/packages/CommonRespeakingRus-1/load'
res = requests.get(url, headers=headers)

print(res)
print(res.text)

url = base_url + '/v1/recognize'
data_raw = open('voice_tmp.wav', 'rb').read()
data_base64 = base64.encodebytes(data_raw)
# print('RAW DATA\n', data_base64[:20])
data = {
  "audio": {
      "data": data_base64.decode('utf-8'),
      "mime": "audio/basic"
  },
  "package_id": "SpontRus-2"
}
data = {
  "audio": {
    "data": "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvbmx5IGJ5IGhpcyByZWFzb24sIGJ1dCAuLi4=",
    "mime": "audio/L16"
  },
  "package_id": "CommonRespeakingRus-1"
}

jsondata = json.dumps(data)
headers = {
    'Content-Type': 'application/json',
    'X-Session-Id': session_id
}

res = requests.post(url, headers=headers, data=jsondata)

print(res)
print(res.text)
