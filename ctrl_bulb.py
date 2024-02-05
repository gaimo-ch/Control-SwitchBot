import time
import hashlib
import hmac
import base64
import uuid
import requests
import getch

# get_id.pyで取得したIDを入力
bulb_1 = 'https://api.switch-bot.com/v1.1/devices/{deviceID}/commands'
bulb_2 = 'https://api.switch-bot.com/v1.1/devices/{deviceID}/commands'

# SwitchBotアプリより取得
token = ''
secret = ''

# ------------------------------パラメータの生成------------------------------

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

def update_parameters():
    global secret_bytes, t, nonce, sign
    secret_bytes = gen_secret(secret)
    t = gen_t()
    nonce = gen_nonce()
    sign = gen_sign(secret_bytes, t, nonce)

# -------------------------------Bulbの制御-----------------------------------

def send(command):
    update_parameters()
    headers = {
        'Authorization': token,
        'sign': sign,
        't': t,
        'nonce': nonce,
        'Content-Type': 'application/json; charset=utf8'
    }
    payload = {
        'command': command,
        'commandType': 'command'
    }

    response = requests.post(bulb_1, headers=headers, json=payload)
    response = requests.post(bulb_2, headers=headers, json=payload)

    if response.status_code == 200:
        print(f'{command}コマンドを実行したよ')
    else:
        print(f'エラー: {response.status_code} - {response.text}')

if __name__ == "__main__":
    try:
        while True:
            try:
                key = getch.getch()
                if key == '1':
                    send('turnOff')
                elif key == '2':
                    send('turnOn')
                else:
                    print('設定されていない入力を検知!!')
            except OverflowError:
                pass
            except KeyboardInterrupt:
                print('プログラムを終了するよ')
                break
    except KeyboardInterrupt:
        print('プログラムを終了するよ')
