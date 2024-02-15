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

# ------------------------------トークン取得------------------------------

def credentials(): # credentials.jsonが存在するか確認し、存在する場合はその中身を読み込む。存在しない場合は入力を促す
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

token, secret = credentials()

# ------------------------------認証機構------------------------------

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

# -------------------------------シーンの制御-----------------------------------

def ctrl_scene(scene_id: str): # main関数から送られたsceneIdを使って、シーンを実行する
    update_parameters()

    headers = {
        'Authorization': token,
        'sign': sign,
        't': t,
        'nonce': nonce,
        'Content-Type': 'application/json; charset=utf8'
    }
    payload = {
        'sceneId': scene_id,
        'commandType': 'command'
    }

    scene_url = f'https://api.switch-bot.com/v1.1/scenes/{scene_id}/execute'

    response = requests.post(scene_url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f'シーンを実行したよ')
    else:
        print(f'エラー: {response.status_code} - {response.text}')

# -------------------------------デバイスの制御-----------------------------------

def ctrl_device(command, parameter): # id_data.jsonから存在する分のdeviceIdを取得して、それぞれに対してコマンドを送る
    update_parameters()

    with open('id_data.json', "r") as json_file:
        json_data = json.load(json_file)

    for device_info in json_data["body"]["deviceList"]:
        if device_info["deviceType"] == "Color Bulb":
            device_id = device_info["deviceId"]
            ctrl_url = 'https://api.switch-bot.com/v1.1/devices/{device_id}/commands'.format(device_id=device_id)

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

            response = requests.post(ctrl_url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f'{command}コマンドを実行したよ')
    else:
        print(f'エラー: {response.status_code} - {response.text}')

# -------------------------------main関数-----------------------------------

def main(stdscr):
    try:
        while True:
            key = stdscr.getch()
            if key == ord('0'): # 0キー
                ctrl_device('turnOff', 'default')
            elif key == curses.KEY_ENTER or key == 10: # Enterキー
                ctrl_scene(scene_id = '') # シーンIDを入力
            elif key == 9: # tabキー
                ctrl_scene(scene_id = '') # シーンIDを入力
            elif key == ord('/'): # /キー
                ctrl_scene(scene_id = '') # シーンIDを入力
            else:
                print('設定されていない入力を検知!!')
    except KeyboardInterrupt:
        print('プログラムを終了するよ')

if __name__ == "__main__":
    curses.wrapper(main)