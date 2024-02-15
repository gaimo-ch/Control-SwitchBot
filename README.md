<h1 align="center">
    💡Control SwitchBot with API
</h1>

---
# 概要


# 🛠 準備をしよう

## トークンを取得
SwitchBotアプリ → プロフィール → 設定 → アプリバージョンを10回ほどタップ → 開発者向けオプション → トークンを取得<br>

## deviceID, sceneIDを取得
get_data.pyを実行すると、トークン, シークレットを求められるので<br>
[トークンを取得](#トークンを取得)にて取得した値を入力してください。

その後、id_data.json, scene_data.jsonが生成されます。 


# ✅ 試してみよう

ctrl_scene.pyを実行し、設定したキーを入力することによってシーンを制御することができます。