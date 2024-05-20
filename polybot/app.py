import flask
from flask import request
import os
from bot import Bot, ImageProcessingBot
from get_docker_secret import get_docker_secret


app = flask.Flask(__name__)

TELEGRAM_TOKEN = get_docker_secret('telegram_bot_token')
TELEGRAM_APP_URL = os.environ['TELEGRAM_APP_URL']
# version test comment

@app.route('/', methods=['GET'])
def index():
    return 'Ok'


@app.route(f'/{TELEGRAM_TOKEN}/', methods=['POST'])
def webhook():
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


if __name__ == "__main__":
    bot = ImageProcessingBot(TELEGRAM_TOKEN, TELEGRAM_APP_URL)

    app.run(host='0.0.0.0', port=8443)
