# Telegram Bot

add to contact: https://t.me/everctf_bot

## everctf_bot.py
bot 主程式
可讀取以下輸入
- /add  : 新增ip
    - 輸入 /add 後依指示輸入ip
- /rm   : 移除ip
    - 輸入 /rm 後依指示輸入ip
- /show : 列出目前的ip
- /save : 儲存目前的ip清單，檔名為chat_id
- /load : 載入先前除存的ip清單
- /run  : 開始偵測
    依chat_id建立process，執行monitor.py
- /stop : 停止偵測
- /help : 列出支援的指令

```
pip install requirements.txt
```

## everctf_bot_api.py
api主程式，flask架構
目前僅有broadcast功能
post /broadcast
data 格式為 {'message':'要廣播的內容'}

## everctf_bot_data.py
放bot的token，可改用自行建立的bot token
應該要放ignore的東西

## monitor.py
偵測ip，目前僅支援ping
受bot控制自動執行
