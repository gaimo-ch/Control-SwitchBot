import json
import time
import hashlib
import hmac
import base64
import uuid
import requests
import sys

# SwitchBotアプリより取得
token = ''
secret = ''

def gen_secret(secret):
    return bytes(secret, 'utf-8')

def gen_sign(secret, t, nonce):
    string_to_sign = '{}{}{}'.format(token, t, nonce)
    string_to_sign = bytes(string_to_sign, 'utf-8')
    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    return sign

def gen_t():
    return str(int(round(time.time() * 1000)))

def gen_nonce():
    return str(uuid.uuid4())

secret_bytes = gen_secret(secret)
t = gen_t()
nonce = gen_nonce()
sign = gen_sign(secret_bytes, t, nonce)

url = 'https://api.switch-bot.com/v1.1/devices/'

headers = {
    'Authorization': token,
    'sign': sign,
    't': t,
    'nonce': nonce,
    'Content-Type': 'application/json; charset=utf8'
}

response = requests.get(url, headers=headers)

# 整形して出力
sys.stdout.reconfigure(encoding='utf-8')
if response.status_code == 200:
    formatted_data = json.dumps(response.json(), indent=2, ensure_ascii=False)
    print(formatted_data)
else:
    print(f"Error: {response.status_code} - {response.text}")
