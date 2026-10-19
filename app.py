import os
import sys
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)

# ดึงค่า Environment Variables
channel_secret = os.getenv("LINE_CHANNEL_SECRET")
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# ตรวจสอบว่าตั้งค่า Environment Variables ครบถ้วนหรือไม่
if not channel_secret or not channel_access_token:
    print("Error: กรุณาตั้งค่า LINE_CHANNEL_SECRET และ LINE_CHANNEL_ACCESS_TOKEN")
    sys.exit(1)

handler = WebhookHandler(channel_secret)
config = Configuration(access_token=channel_access_token)

@app.route("/")
def home():
    return "LINE Webhook is running"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        app.logger.error(f"Error handling webhook: {e}")
        abort(500)

    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(config) as api_client:
        api = MessagingApi(api_client)

        api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(
                        text="สวัสดีครับ LINE Bot ทำงานแล้ว"
                    )
                ]
            )
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)