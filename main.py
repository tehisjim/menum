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
        "#泰泰我要": "[img]https://i.imgur.com/yMXYZON.png[/img]",
        "#二苓市場羊肉": "[img]https://i.imgur.com/rv0aH8d.png[/img]",
        "#桌上賓": "[img]https://i.imgur.com/6BzJDlf.png[/img]",
        "#日初": "[img]https://i.imgur.com/x2mFPeN.png[/img]",
        "#悟饕": "[img]https://i.imgur.com/joT4piG.png[/img]",
        "#正忠": "[img]https://i.imgur.com/9515Cm0.png[/img]",
        "#雙饗丼": "[img]https://i.imgur.com/R6YNwWV.png[/img]",
        "#廣招英": "[img]https://i.imgur.com/GvQwtlm.png[/img]",
        "#福樺": "[img]https://i.imgur.com/K5p9ajC.png[/img]",
        "#小丸子牛排": "[img]https://i.imgur.com/cSJ7EsX.png[/img]",
        "#NU": "[img]https://i.imgur.com/zQCxhCA.png[/img]",
        "#食扒穗": "[img]https://i.imgur.com/s5GLQ4a.png[/img]",
        "#八方": "[img]https://i.imgur.com/DXByKl5.png[/img]",
        "#21世紀": "[img]https://i.imgur.com/NN1YHjJ.png[/img]",
        "#麻古": "[img]https://i.imgur.com/QMD5RXQ.png[/img]",
        "#黑白馬飯捲": "[img]https://i.imgur.com/k0089Fx.png[/img]",
        "#水巷茶弄": "[img]https://i.imgur.com/jAHJPxh.png[/img]",
        "#可不可": "[img]https://i.imgur.com/8Si5bxB.png[/img]",
        "#也竹": "[img]https://i.imgur.com/u6zSKLV.png[/img]",
        "#茶湯會": "[img]https://i.imgur.com/7z3EElA.png[/img]",
        "#丸食屋": "[img]https://i.imgur.com/6sJnNeZ.png[/img]",
        "#拉亞": "[img]https://i.imgur.com/eiTdnbX.jpeg[/img]",
        "#德耀": "[img]https://i.imgur.com/PIh7oSq.png[/img]",
        "#八廚": "[img]https://i.imgur.com/8LDLY7G.jpeg[/img]",
        "#宜賓": "[img]https://i.imgur.com/OtwK6Ji.jpeg[/img]",
        "#老賴": "[img]https://i.imgur.com/HNaj1kb.png[/img]",
        "#沾武士": "[img]https://i.imgur.com/upMdo7S.jpeg[/img]",
        "#勁請享用": "[img]https://i.imgur.com/NJ9p4rA.jpeg[/img]",
        "#珍好味": "[img]https://i.imgur.com/rbtv9l6.jpeg[/img]",
        "#黃悶雞": "[img]https://i.imgur.com/zb3CWa9.jpeg[/img]",
        "#福烏龍麵": "[img]https://i.imgur.com/uaZYn0C.jpeg[/img]",
        "#蘭州": "[img]https://i.imgur.com/1I4DvJD.jpeg[/img]",
    }

    # 關鍵字對應文字（自動產生菜單）
    menu_keywords = "\n".join(sorted(keyword_images.keys()))
    keyword_replies = {
        "#菜單": "🍔 目前菜單的關鍵字有：\n" + menu_keywords
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
