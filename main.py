from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import os

app = Flask(__name__)

# 從環境變數讀取
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    print("Request body:", body)  # debug 用

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
        "#五十嵐": "https://blog-media-cdn.roo.cash/blog/wp-content/uploads/2024/07/26011730/447387930_979502500629595_5781678396354667473_n-768x1046.jpg",
        "#時光": "https://i.imgur.com/4BV40Mr.png",
        "#公仔麵": "https://i.imgur.com/qSwXGeF.png",
        "#晨間": "https://i.imgur.com/Yiz5pZg.png",
        "#清心": "https://i.imgur.com/EwP4WVP.png",
        "#美之城": ["https://i.imgur.com/eht90P2.png", "https://i.imgur.com/IERCqqd.png"],
        "#一流": "https://i.imgur.com/GTH3tnj.png",
        "#克里姆": "https://i.imgur.com/hU31toV.png",
        "#大眾羊肉": "https://i.imgur.com/e69rDum.png",
    }

    # 關鍵字對應文字
    keyword_replies = {
        "#菜單": "🍔 目前支援的關鍵字有：\n#丹丹\n#五十嵐\n#公仔麵\n#晨間\n#清心\n#美之城\n#一流\n#克里姆\n#大眾羊肉"
    }

    if user_text in keyword_images:
        img_url = keyword_images[user_text]
        if isinstance(img_url, list):  # 多張圖片
            reply = [ImageSendMessage(
                original_content_url=url, preview_image_url=url) for url in img_url]
        else:
            reply = ImageSendMessage(
                original_content_url=img_url, preview_image_url=img_url)
    elif user_text in keyword_replies:
        reply = TextSendMessage(text=keyword_replies[user_text])
    else:
        pass

    line_bot_api.reply_message(event.reply_token, reply)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
