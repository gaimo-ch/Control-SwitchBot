import time
import hashlib
import hmac
import base64
import uuid
import requests
import curses
from rich.console import Console
from typing import Optional
import typer
import os
import json

app = typer.Typer()

# get_id.pyで取得したIDを入力
bulb_1 = 'https://api.switch-bot.com/v1.1/devices//commands'
bulb_2 = 'https://api.switch-bot.com/v1.1/devices//commands'

def load_credentials():
    credentials_file = "credentials.json"
    if os.path.exists(credentials_file):
        with open(credentials_file) as f:
            credentials = json.load(f)
            return credentials.get("token"), credentials.get("secret")
    else:
        console = Console()
        console.print("Credentials file not found. Please enter your token and secret.")
        token = console.input("Token: ")
        secret = console.input("Secret: ")
        credentials = {"token": token, "secret": secret}
        with open(credentials_file, "w") as f:
            json.dump(credentials, f)
        return token, secret

token, secret = load_credentials()

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

def send(command, parameter):
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
        'parameter': parameter,
        'commandType': 'command'
    }

    response = requests.post(bulb_1, headers=headers, json=payload)
    response = requests.post(bulb_2, headers=headers, json=payload)

    if response.status_code == 200:
        print(f'{command}コマンドを実行したよ')
    else:
        print(f'エラー: {response.status_code} - {response.text}')

def main(stdscr):
    try:
        while True:
            key = stdscr.getch()
            if key == ord('0'):
                send('turnOff', 'default')
            elif key == curses.KEY_ENTER or key == 10:
                send('setColor', '255:255:255') # 白
                send('setBrightness', '100')   
                send('setColorTemperature', '6500')
            elif key == 9:
                send('setColor', '255:82:51') # 橙
                send('setBrightness', '50')
            elif key == ord('7'):
                send('setColor', '255:82:51') # 橙・輝度弱め
                send('setBrightness', '5')     
            elif key == ord('/'): # tab
                send('setColor', '138:64:191') # 紫
                send('setBrightness', '100')   
            else:
                print('設定されていない入力を検知!!')
    except KeyboardInterrupt:
        print('プログラムを終了するよ')

if __name__ == "__main__":
    curses.wrapper(main)