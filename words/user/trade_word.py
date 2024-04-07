import config
from data import db
from decimal import Decimal

cannot_open_trade_yourself = "<i>Нельзя открыть сделку самим собой. Пожалуйста попробуйте заново.</i>"
seller_not_found = "<i>К сожалению пользователь не найден. Пожалуйста попробуйте заново.</i>"
wrong_id_or_name = "<i>Ой что-то пошло не так. Пожалуйста попробуйте писат username или ID.</i>"
choose_coin = "<b>💳 Выберите валюту сделки:</b>"
trade_canceled = "<i>Сделка успешна отменена.</i>"
wrong_input_amount = "<i>Нельзя использовать запитую «,». Пожалуйста используйте точки «.».</i>"
not_enough_money = "<i>В балансе не хватает денег. Пожалуйста пополните баланс и попробуйте заново.</i>"
min_trade_desc = "<i>Опишите условия сделки подробно. Пожалуйста попробуйте заново.</i>"
trade_desc = ("<b>Что будете покупать у продавьца?</b> <i>(Обязательно опишите условия сделки подробнее. Условия "
              "сделки помогут вам решать спор)</i>\n\n<b>Напишите условия сделки:</b>")
waiting_confirm_trade_seller = "<b>Ожидаем ответа продавца. Пожалуйста подождите!</b>"
empty_page = "Пустая страница"
trade_close = "<b>Вы уверены завершить сделку?</b>"
write_feedback = "<b>Напишите отзыв о продавце.</b> "
not_enough_feedback = "<b>Пожалуйста пишите отзыв подробнее.</b>"
dismute = "<b>Объясните пожалуйста что пошло не так?</b> <i>(Опишите ситуацию подробнее).</i>"
not_enough_dismute = "Пожалуйста oпишите ситуацию подробнее."
open_dismute = "\n\n<b>Отправлено. Администратор свяжется с вами в ближайшее время. Ожидайте!</b>"
try_again = "<i>Пожалуйста попробуйте заново.</i>"
error_delete_message = "<i>Ошибка 400</i>"


def seller_profile(seller_data):
    number_trade = db.number_closed_trades(seller_data['userid'])

    text = f"""<b>👤 Об аккаунте</b>
<b>┌ </b><i><b>Имя: </b><code>{seller_data['fullname']}</code></i>
<b>├ </b><i><b>Логин: </b>{seller_data['username']}</i>
<b>└ </b><i><b>ID аккаунта: </b><code>{seller_data['userid']}</code></i>

<b>📊 Сделки</b>
<b>┌ </b><i><b>Покупок: </b>{number_trade[0]}</i>
<b>└ </b><i><b>Продаж: </b>{number_trade[1]}</i>"""

    return text


def seller_feedbacks(user_id, page=1):
    global text

    feedbacks_data = db.get_user_feedbacks(user_id, page)

    if feedbacks_data:
        text = ""

        for item in feedbacks_data:
            user_data = db.get_user_data(user_id=item[2])

            if user_data is not None:
                text += f"""<b>┌<i> Пользователь: </i></b><i><a href='t.me/{user_data['username'][1:]}'>{user_data['fullname']}</a></i>
<b>├<i> Дата: </i></b><i>{item[5]}</i>
<b>└<i> Отзыв: </i></b><i>{item[4]}</i>\n\n"""

    else:
        text = "<b>Список пуст</b>"

    return text


def amount(userid, coin):
    user_data = db.get_user_data(userid=userid)
    user_balance = "{:.2f}".format(float(user_data[config.CURRENCY[coin] + "_balance"])) if config.CURRENCY[
                                                                                                coin] == "rub" or \
                                                                                            config.CURRENCY[
                                                                                                coin] == "usd" else "{:.8f}".format(
        float(user_data[config.CURRENCY[coin] + "_balance"]))

    text = f"""<b>💳 Ваш {config.CURRENCY[coin].upper()} баланс:</b> <code>{user_balance}{config.CURRENCY_ICON[coin]}</code>

<b>Введите сумму сделки:</b>"""

    return text


def wrong_amount(coin):
    global text

    if config.CURRENCY[coin] == "rub" or config.CURRENCY[coin] == "usd":
        text = "<i>Сумма не может содержать более 3 десятичных знаков.</i>"

    elif config.CURRENCY[coin] == "btc":
        text = "<i>Сумма не может содержать более 8 десятичных знаков.</i>"

    return text


def trade_min_amount(coin):
    text = f"<i>Минимальная сумма сделки <code>{config.TRADE_LIMIT_CURRENCY_AMOUNT[coin]}{config.CURRENCY[coin].upper()}</code> {'(~1$)' if coin == 2 else ''}.</i>"

    return text


def confirm_trade(trade_data, trade_desc):
    global text

    seller_data = db.get_user_data(user_id=trade_data['seller_id'])
    if trade_data['coin'] == 2:
        btc_amount_rate = Decimal("{:.2f}".format(float(float(trade_data['amount']) * float(config.BTCUSDT_RATE))))

        text = f"""<b>📂 Информация сделки</b>
<b>┌ </b><i><b>Продавец: </b><a href='t.me/{seller_data['username'][1:]}'>{seller_data['fullname']}</a></i>
<b>├ </b><i><b>Сумма: </b><code>{trade_data['amount']}{config.CURRENCY_ICON[trade_data['coin']]}</code> (~{btc_amount_rate}$)</i>
<b>└ </b><i><b>Условия: </b>{trade_desc}</i>"""

    else:
        text = f"""<b>📂 Информация сделки</b>
<b>┌ </b><i><b>Продавец: </b><a href='t.me/{seller_data['username'][1:]}'>{seller_data['fullname']}</a></i>
<b>├ </b><i><b>Сумма: </b><code>{trade_data['amount']}{config.CURRENCY_ICON[trade_data['coin']]}</code></i>
<b>└ </b><i><b>Условия: </b>{trade_desc}</i>"""

    return text


def confirm_trade_seller(trade_data):
    global text

    customer_data = db.get_user_data(user_id=trade_data['customer_id'])

    if trade_data['coin'] == 2:
        btc_amount_rate = Decimal("{:.2f}".format(float(float(trade_data['amount']) * float(config.BTCUSDT_RATE))))

        text = f"""<b>📂 Новая сделка</b>
<b>┌ </b><i><b>Покупатель: </b><a href='t.me/{customer_data['username'][1:]}'>{customer_data['fullname']}</a></i>
<b>├ </b><i><b>Сумма: </b><code>{trade_data['amount']}{config.CURRENCY_ICON[trade_data['coin']]}</code> (~{btc_amount_rate}$)</i>
<b>└ </b><i><b>Условия: </b>{trade_data['desc']}</i>"""

    else:
        text = f"""<b>📂 Новая сделка</b>
<b>┌ </b><i><b>Покупатель: </b><a href='t.me/{customer_data['username'][1:]}'>{customer_data['fullname']}</a></i>
<b>├ </b><i><b>Сумма: </b><code>{trade_data['amount']}{config.CURRENCY_ICON[trade_data['coin']]}</code></i>
<b>└ </b><i><b>Условия: </b>{trade_data['desc']}</i>"""

    return text


def show_trade_data(trade_id, action, userid=None, hide=None):
    global text, trade_amount, btc_amount_rate

    trade_data = db.get_trade_data(trade_id)

    status_trade = {
        1: ["Отказан", "был отказан", "⛔️"],
        2: ["Ожидание", "была принято", "⏳"],
        3: ["Закрыта", "была успешно закрыта", "✅"],
        4: ["Заморожен", "был заморожен", "🔒"]
    }

    user_act_swap = {
        "customer": ["seller", "Продавец"],
        "seller": ["customer", "Покупатель"]
    }

    if action == 0:
        text = f"<b>Сделка №: <code>{trade_data['id']}</code> {status_trade[trade_data['status']][1]}</b>"

    elif action == 1:
        user_act = "customer" if trade_data["customer_id"] == db.get_user_id(userid) else "seller"
        user_data = db.get_user_data(user_id=trade_data[user_act_swap[user_act][0] + "_id"])
        trade_amount = '{:.2f}'.format(float(trade_data['amount'])) if trade_data['coin'] == 0 or trade_data['coin'] == 1 else '{:.8f}'.format(float(trade_data['amount']))
        btc_amount_rate = f"(~{Decimal('{:.2f}'.format(float(float(trade_data['amount']) * float(config.BTCUSDT_RATE))))}$)" if trade_data['coin'] == 2 else ""

        if trade_data['status'] == 1 or trade_data['status'] == 2:
            text = f"""<b>📂 Информация сделки</b>
<b>┌ </b><i><b>Сделка №: </b><code>{trade_data['id']}</code></i>
<b>├ </b><i><b>{user_act_swap[user_act][1]}: </b><a href='t.me/{user_data['username'][1:]}'>{user_data['fullname']}</a></i>
<b>├ </b><i><b>Сумма: </b><code>{trade_amount}{config.CURRENCY_ICON[trade_data['coin']]}</code>{btc_amount_rate}</i>
<b>├ </b><i><b>Условия: </b>{trade_data['desc']}</i>
<b>└ </b><i><b>Статус: </b>{status_trade[trade_data['status']][0]} {status_trade[trade_data['status']][2]}</i>"""

        elif trade_data['status'] == 3:
            feedback = db.get_trade_feedback(trade_data['id'])

            text = f"""<b>📂 Информация сделки</b>
<b>┌ </b><i><b>Сделка №: </b><code>{trade_data['id']}</code></i>
<b>├ </b><i><b>{user_act_swap[user_act][1]}: </b><a href='t.me/{user_data['username'][1:]}'>{user_data['fullname']}</a></i>
<b>├ </b><i><b>Сумма: </b><code>{trade_amount}{config.CURRENCY_ICON[trade_data['coin']]}</code>{btc_amount_rate}</i>
<b>├ </b><i><b>Условия: </b>{trade_data['desc']}</i>
<b>├ </b><i><b>Отзыв: </b>{'Отсутствует' if feedback is None else feedback}</i>
<b>└ </b><i><b>Статус: {status_trade[trade_data['status']][0]} ✅</b></i>

{'<b>Спасибо вам что используете наш <u>Гарант Бот ⭐</u></b>' if hide is None else ''}"""

        elif trade_data['status'] == 4:
            dispute_data = db.get_dispute_data(trade_data['id'])
            dispute_open_person = db.get_user_data(user_id=dispute_data['who_open_id'])

            text = f"""<b>📂 Информация сделки</b>
<b>┌ </b><i><b>Сделка №: </b><code>{trade_data['id']}</code></i>
<b>├ </b><i><b>{user_act_swap[user_act][1]}: </b><a href='t.me/{user_data['username'][1:]}'>{user_data['fullname']}</a></i>
<b>├ </b><i><b>Сумма: </b><code>{trade_amount}{config.CURRENCY_ICON[trade_data['coin']]}</code>{btc_amount_rate}</i>
<b>├ </b><i><b>Условия: </b>{trade_data['desc']}</i>
<b>├ </b><i><b>Статус: </b>{status_trade[trade_data['status']][0]} {status_trade[trade_data['status']][2]}</i>
<b>├ </b><i><b>Заморозил: </b><a href='t.me/{dispute_open_person['username'][1:]}'>{dispute_open_person['fullname']}</a></i>
<b>└ </b><i><b>Причина: </b>{dispute_data['reason']}</i>"""

    elif action == 2:
        feedback = db.get_trade_feedback(trade_data['id'])

        if feedback:
            text = f"""<b>📢 Сделка № <code>{trade_data['id']}</code> сумма <code>{trade_amount}{config.CURRENCY_ICON[trade_data['coin']]}</code>{btc_amount_rate} от {db.get_user_username(user_id=trade_data['customer_id'])} для {db.get_user_username(user_id=trade_data['seller_id'])} была успешно закрыта.</b>\n
<b>Отзыв: </b><i>{feedback}.</i>"""

        else:
            text = f"<b>📢 Сделка № <code>{trade_data['id']}</code> сумма <code>{trade_amount}{config.CURRENCY_ICON[trade_data['coin']]}</code>{btc_amount_rate} от {db.get_user_username(user_id=trade_data['customer_id'])} для {db.get_user_username(user_id=trade_data['seller_id'])} была успешно закрыта.</b>"

    return text
