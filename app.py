from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import os

app = Flask(__name__)

# 從環境變數讀取
CHANNEL_ACCESS_TOKEN = "UMuvfMQIByqYrGLo1Qd0P+JNXwPRDwoCHuEjCpPZIBwZ54EawekgENrUzITg8lM+XGwcw+KqdxswTVt2o6gWmzE59zPl6z+BZKdBX7DyCT7p1uxmRt6TCYH77n/DInyXaK3Se1NeosnTuE0o+PKlugdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "e5b8caec53a390ee74ccbefa801c7fc6"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()

    # 關鍵字對應圖片
    keyword_images = {
        "#丹丹": "https://cpok.tw/wp-content/uploads/2025/02/2025.jpeg",
        "#狗狗": "https://thumb.photo-ac.com/f1/f16b270bc3660676926c5e41f7cdc383_t.jpeg",
        "測試": "https://i.imgur.com/xHgkP4r.png"
    }

    if user_text in keyword_images:
        img_url = keyword_images[user_text]
        reply = ImageSendMessage(
            original_content_url=img_url,
            preview_image_url=img_url
        )
    else:
        reply = TextSendMessage(text="這個關鍵字沒有圖片 😅")

    line_bot_api.reply_message(event.reply_token, reply)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
