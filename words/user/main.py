import config

from routers.func import remove_html_tags
from decimal import Decimal
from data import db

# Words
welcome = """<b>🤵🏻 Добро пожаловать</b>\n
<b>Бот предназначен</b> - для проведения безопасных сделок обоих участников.\n
📑 <b>Сервис взимает комиссию в 4% и комиссия от платежных систем.</b>"""
none_username = "<b>Вам необходимо нужно установить <i>@username</i> для работы с ботом!</b>"
search_seller = """<b>Для поиска пользователя</b>
   <i>1. Напишите username боту (например -> @username)
   2. Напишите ID боту (ID можно узнать в разделе -> 👤 Мой профиль</i>"""
captcha = "<b>Введите число в картинке:</b>"
all_trades = "<b>Выберите подходящию сделку:</b>"
optional = "<b>Дополнительно:</b>"
type_trade = "<b>Выберите тип сделок:</b>"
trade = "<b>Выберите вид сделки:</b>"
faq = "<b>Часто задаваемые вопросы:</b>"
antispam = "<b>🛡️Антиспам активирован. Бот будет работать через час.</b>"
antispam_stop = "<b>❗️Бот начал работать. Пожалуйста не спамте следующий раз.</b>"
antispam_working = "Активирована антиспам. Данный момент бот не работает"


def profile(userid):
    user_data = db.get_user_data(userid=userid)
    number_trade = db.number_closed_trades(userid)

    user_balance_rate = {
        "rubusdt": Decimal("{:.2f}".format(float(float(user_data['usd_balance']) * float(config.RUBUSD_RATE)))),
        "btcusdt": Decimal("{:.2f}".format(float(float(user_data['btc_balance']) * float(config.BTCUSDT_RATE))))
    }

    text = f"""<b>👤 Об аккаунте</b>
<b>┌ </b><i><b>Имя: </b><code>{remove_html_tags(user_data['fullname'])}</code></i>
<b>├ </b><i><b>Логин: </b>{user_data['username']}</i>
<b>└ </b><i><b>ID аккаунта: </b><code>{user_data['userid']}</code></i>

<b>💳 Баланс</b>
<b>┌ </b><i><b>RUB: </b><code>{'{:.2f}'.format(float(user_data['rub_balance']))}₽</code></i>
<b>├ </b><i><b>USD: </b><code>{'{:.2f}'.format(float(user_data['usd_balance']))}$</code> (~{user_balance_rate['rubusdt']}₽)</i>
<b>└ </b><i><b>BTC: </b><code>{"{:.8f}".format(float(user_data['btc_balance']))}BTC</code> (~{user_balance_rate['btcusdt']}$)</i>

<b>📊 Сделки</b>
<b>┌ </b><i><b>Покупок: </b>{number_trade[0]}</i>
<b>└ </b><i><b>Продаж: </b>{number_trade[1]}</i>

<b>💹 Курс валют</b>
<b>┌ </b><i><b>USD: </b>{'{:.2f}'.format(float(config.RUBUSD_RATE))}₽</i>
<b>└ </b><i><b>BTC: </b>{'{:.2f}'.format(float(config.BTCUSDT_RATE))}$</i>"""

    return text


def paginator_trades(number_active_trades, ua, status):
    global text

    if number_active_trades:
        action_dict = {
            0: "Покупок",
            1: "Продаж"
        }

        if status == 2:
            text = f"<b>Активные сделки</b> ➡️ <b>{action_dict[ua]}:</b>"

        elif status == 3:
            text = f"<b>История сделок</b> ➡️ <b>{action_dict[ua]}:</b>"

    else:
        text = "<b>Список пуст</b>"

    return text
