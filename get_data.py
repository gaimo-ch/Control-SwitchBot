import json
import time
import hashlib
import hmac
import base64
import uuid
import requests
import sys
from rich.console import Console
from typing import Optional
import typer
import os

app = typer.Typer()
sys.stdout.reconfigure(encoding='utf-8')

def credentials():
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

# SwitchBotアプリより取得

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

@app.command('id')
def get_id():
    """
    Save the deviceID data as JSON in the current directory.
    """
    url = 'https://api.switch-bot.com/v1.1/devices/'

    headers = {
        'Authorization': token,
        'sign': sign,
        't': t,
        'nonce': nonce,
        'Content-Type': 'application/json; charset=utf8'
    }

    response = requests.get(url, headers=headers)

    # 整形して出力する jsonがなければ新規作成する
    if response.status_code == 200:
        id_data = json.dumps(response.json(), indent=2, ensure_ascii=False)
        print(id_data)
        with open('id_data.json', 'w') as f:
            json.dump(response.json(), f, indent=2)
        print("DeviceID data saved successfully.")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    
@app.command('scene')
def get_scene():
    """
    Save the scene data as JSON in the current directory.
    """
    url = 'https://api.switch-bot.com/v1.1/scenes'

    headers = {
        'Authorization': token,
        'sign': sign,
        't': t,
        'nonce': nonce,
        'Content-Type': 'application/json; charset=utf8'
    }

    response = requests.get(url, headers=headers)

    # 整形して出力する jsonがなければ新規作成する
    if response.status_code == 200:
        scene_data = response.json()
        scene_data = json.dumps(response.json(), indent=2, ensure_ascii=False)
        print(scene_data)
        with open('scene_data.json', 'w') as f:
            json.dump(response.json(), f, indent=2)
        print("Scene data saved successfully.")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    

if __name__ == '__main__':
    app()