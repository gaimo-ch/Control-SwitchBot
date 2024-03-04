<h1 align="center">
    🪄💡Control SwitchBot with API🪄💡
</h1>
<h3 align="center">
    Python 3.12.2 / Debian GNU/Linux 12 / SwitchBot API v1.1
</h3>

---
# 📜 概要

Numpadをお望みの通りに割り当てて、Color Bulbを制御することができるよ🪄💡

# 🛠 準備をしよう

## 認証
SwitchBotアプリ → プロフィール → 設定 → アプリバージョンを10回ほどタップ → 開発者向けオプション → トークンを取得

get_data.pyを実行すると、トークン, シークレットを求められるので
取得した値を入力してください。

その後、id_data.json, scene_data.jsonが生成されます。 

## キーマッピング
ctrl_scene.pyにお望みのキー及びsceneIDを指定してください。

# ✅ 試してみよう

ctrl_scene.pyを実行し、設定したキーを入力することによってシーンを制御することができます。

# 🫲 補足

ctrl_device関数が存在する理由は、sceneでbulbをオフにすると変な挙動をするので、あえてturnOffコマンドを送信するためです。

# 🔖 参考

https://github.com/OpenWonderLabs/SwitchBotAPI
