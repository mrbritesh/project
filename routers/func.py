import config
import asyncio
import re
import random
import requests

from PIL import Image
from captcha.image import ImageCaptcha
from binance.client import Client

from words.user import main


def create_captcha(userid):
    image = ImageCaptcha()
    captcha_code = "".join(random.choices('0123456789', k=6))
    image_captcha = image.generate(captcha_code)
    image_path = f"routers/captcha-{userid}.png"
    Image.open(image_captcha).resize((300, 100)).save(image_path)

    return captcha_code, image_path


def remove_html_tags(tag_text):
    clean_text = re.sub(r'<[^>]*>', '', tag_text)
    return clean_text


def get_btcusdt_rate():
    client = Client(config.BINANCE_API, config.BINANCE_SECRETKEY)
    return client.get_avg_price(symbol='BTCUSDT')['price']


def get_currency_rate():
    URL = f"https://openexchangerates.org/api/latest.json?&base=USD&symbols=RUB"
    response = requests.get(URL, headers={"Authorization": f"Token {config.OPENEXCHANGE_API}"})
    data = response.json()
    return data['rates']['RUB']


async def update_rubusd_rate():
    while True:
        config.RUBUSD_RATE = get_currency_rate()
        await asyncio.sleep(43200)


async def update_btcusd_rate():
    while True:
        config.BTCUSDT_RATE = get_btcusdt_rate()
        config.TRADE_LIMIT_CURRENCY_AMOUNT[2] = "{:.8f}".format(float(1 / float(get_btcusdt_rate())))
        await asyncio.sleep(5)


async def antispam(msg=None, call=None):
    if msg:
        if (config.USER_MESSAGE_COUNT.get(msg.from_user.id, 0) >= config.SPAM_THRESHOLD and
                (msg.date - config.USER_LAST_MESSAGE_TIME[msg.from_user.id]).total_seconds() < 3600):
            return False

        else:
            if msg.from_user.id in config.USER_LAST_MESSAGE_TIME:
                time_elapsed = (msg.date - config.USER_LAST_MESSAGE_TIME[msg.from_user.id]).total_seconds()

                if time_elapsed <= config.SPAM_INTERVAL:
                    config.USER_MESSAGE_COUNT[msg.from_user.id] += 1

                else:
                    config.USER_MESSAGE_COUNT[msg.from_user.id] = 1

            config.USER_LAST_MESSAGE_TIME[msg.from_user.id] = msg.date

            if config.USER_MESSAGE_COUNT.get(msg.from_user.id, 0) == config.SPAM_THRESHOLD:
                config.USERS_SPAM[msg.from_user.id] = 1
                await msg.answer(main.antispam)
                await asyncio.sleep(3600)

                config.USERS_SPAM.pop(msg.from_user.id)
                config.USER_MESSAGE_COUNT.pop(msg.from_user.id)
                await msg.answer(main.antispam_stop)

                return False

            return True

    elif call:
        if call.from_user.id in config.USERS_SPAM:
            await call.answer(main.antispam_working, show_alert=True)
            return False

        else:
            return True
