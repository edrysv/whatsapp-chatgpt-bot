import os
from flask import Flask, request
import openai
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
ultramsg_instance = os.getenv("ULTRAMSG_INSTANCE")
ultramsg_token = os.getenv("ULTRAMSG_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return "No data", 400

    message = data.get("body", {}).get("text", "")
    sender = data.get("from", "")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты вежливый помощник для клиентов бизнеса."},
            {"role": "user", "content": message}
        ]
    )
    reply = response['choices'][0]['message']['content']

    url = f"https://api.ultramsg.com/{ultramsg_instance}/messages/chat"
    payload = {
        "token": ultramsg_token,
        "to": sender,
        "body": reply
    }
    requests.post(url, data=payload)

    return "ok", 200

if __name__ == "__main__":
    app.run()
