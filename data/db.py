import sqlite3
import datetime
import config

from decimal import Decimal

datetime = datetime.datetime.now()
date = f"{datetime.day}.{datetime.month}.{datetime.year}"
time = f"{datetime.strftime('%H')}:{datetime.strftime('%M')}"

connect = sqlite3.connect("database.db")
cursor = connect.cursor()

# Items
user_items = ['id', 'userid', 'fullname', 'username', 'rub_balance',
              'usd_balance', 'btc_balance', 'status', 'ban', 'date']
feedback_items = ['id', 'trade_id', 'customer_id', 'seller_id', 'feedback', 'date']
trade_items = ['id', 'customer_id', 'seller_id', 'coin', 'amount', 'desc', 'status', 'date']
dispute_items = ['trade_id', 'who_open_id', 'who_for_id', 'reason', 'status', 'date']


# bot_version_items = ['id', 'bot_version', 'date']


def add_tables():
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY UNIQUE,
                        userid INTEGER NOT NULL UNIQUE,
                        fullname VARCHAR NOT NULL,
                        username VARCHAR NOT NULL,
                        rub_balance  VARCHAR NULL,
                        usd_balance VARCHAR NOT NULL,
                        btc_balance VARCHAR NOT NULL,
                        status INTEGER NOT NULL,
                        ban INTEGER NOT NULL,
                        date TEXT NOT NULL ) """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS trades (
                        id INTEGER PRIMARY KEY UNIQUE,
                        customer_id INTEGER NOT NULL,
                        seller_id INTEGER NOT NULL,
                        coin INTEGER NOT NULL,
                        amount VARCHAR NOT NULL,
                        desc TEXT NOT NULL,
                        status INTEGER NOT NULL,
                        date TEXT NOT NULL ) """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS disputes (
                        trade_id INTEGER NOT NULL UNIQUE,
                        who_open_id INTEGER NOT NULL,
                        who_for_id INTEGER NOT NULL,
                        reason VARCHAR NOT NULL,
                        status INTEGER NOT NULL,
                        date TEXT NOT NULL )""")

    # cursor.execute(""" CREATE TABLE withdraws (
    #                     ID INTEGER PRIMARY KEY UNIQUE,
    #                     userId INTEGER NOT NULL,
    #                     coin TEXT NOT NULL,
    #                     amount FLOAT NOT NULL,
    #                     status TEXT NOT NULL,
    #                     date TEXT NOT NULL ) """)

    # cursor.execute(""" CREATE TABLE IF NOT EXISTS users_version (
    #                     ID INTEGER PRIMARY KEY UNIQUE,
    #                     userId INTEGER UNIQUE NOT NULL,
    #                     version FLOAT NOT NULL,
    #                     date TEXT NOT NULL ) """)

    # cursor.execute(""" CREATE TABLE IF NOT EXISTS admins_roles (
    #                     ID INTEGER PRIMARY KEY UNIQUE,
    #                     role_full_name VARCHAR NOT NULL,
    #                     role_name VARCHAR NOT NULL) """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS admins (
                        id INTEGER PRIMARY KEY UNIQUE,
                        userid INTEGER NOT NULL,
                        fullname VARCHAR NOT NULL,
                        username VARCHAR NOT NULL,
                        status TEXT NOT NULL,
                        date TEXT NOT NULL) """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS feedbacks (
                        id INTEGER PRIMARY KEY,
                        trade_id INTEGER NOT NULL,
                        customer_id INTEGER NOT NULL,
                        seller_id INTEGER NOT NULL,
                        feedback TEXT(300),
                        date TEXT NOT NULL) """)

    connect.commit()


def add_user(userid, fullname, username):
    cursor.execute(f" SELECT * FROM users WHERE userid = {userid} ")
    user_data = cursor.fetchone()

    if user_data is None:
        cursor.execute(f""" INSERT INTO users (userid, fullname, username, rub_balance, usd_balance, btc_balance,
        status, ban, date) VALUES ({userid}, '{fullname}', '@{username.lower()}', 0, 0, 0, 0, 0, '{date}') """)

        connect.commit()

    else:
        cursor.execute(
            f" UPDATE users SET fullname = '{fullname}', username = '@{username.lower()}' WHERE userid = {userid} ")
        connect.commit()

    return user_data


def get_user_data(user_id=None, userid=None, username=None):
    if user_id and userid is None and username is None:
        cursor.execute(f""" SELECT * FROM users WHERE id = {user_id} """)

    elif userid and user_id is None and username is None:
        cursor.execute(f""" SELECT * FROM users WHERE userid = {int(userid)} """)

    elif username and user_id is None and userid is None:
        cursor.execute(f""" SELECT * FROM users WHERE username = '{username.lower()}' """)

    data = cursor.fetchall()

    user_data = {}
    count = 0

    if data:
        for item in user_items:
            user_data[item] = data[0][count]
            count += 1

    else:
        user_data = None

    return user_data


def get_userid(user_id):
    cursor.execute(f""" SELECT userid FROM users WHERE id = {user_id} """)
    return cursor.fetchone()[0]


def get_user_id(userid):
    cursor.execute(f""" SELECT id FROM users WHERE userid = {userid} """)
    return cursor.fetchone()[0]


def get_user_username(user_id=None, userid=None):
    if user_id is not None and userid is None:
        cursor.execute(f""" SELECT username FROM users WHERE id = {user_id} """)

    elif user_id is None and userid is not None:
        cursor.execute(f""" SELECT username FROM users WHERE userid = {userid} """)

    return cursor.fetchone()[0]


def get_user_feedbacks(user_id, page=1):
    cursor.execute(
        f""" SELECT * FROM feedbacks WHERE seller_id = {user_id} ORDER BY ID DESC LIMIT {(page - 1) * 5}, 5""")
    return cursor.fetchall()


def number_user_feedback(user_id):
    cursor.execute(f" SELECT COUNT(*) FROM feedbacks WHERE seller_id = {user_id} ")
    return cursor.fetchone()[0]


def add_trade(userid, data):
    global new_balance, trade_amount

    cursor.execute(f""" SELECT {config.CURRENCY[data['coin']] + '_balance'} FROM users WHERE userid = {userid} """)

    if data['coin'] == 0 or data['coin'] == 1:
        new_balance = Decimal("{:.2f}".format(float(cursor.fetchone()[0]) - float(data['amount'])))
        trade_amount = Decimal("{:.2f}".format(float(data['amount'])))

    elif data['coin'] == 2:
        new_balance = Decimal("{:.8f}".format(float(cursor.fetchone()[0]) - (float(data['amount']))))
        trade_amount = Decimal("{:.8f}".format(float(data['amount'])))

    cursor.execute(f""" UPDATE users SET {config.CURRENCY[data['coin']] + '_balance'} = {new_balance} 
                        WHERE userid = {userid} """)

    cursor.execute(f""" INSERT INTO trades (customer_id, seller_id, coin, amount, desc, status, date) VALUES (
                        {data['customer_id']}, {data['seller_id']}, {data['coin']}, 
                        {trade_amount}, '{data['desc']}', '0', '{date}') """)
    connect.commit()

    cursor.execute(f""" SELECT id FROM trades WHERE id = (select max(id) from trades) 
        AND customer_id = {data['customer_id']} AND seller_id = {data['seller_id']} AND coin = {data['coin']} 
        AND amount = {trade_amount} AND desc = '{data['desc']}' """)

    return cursor.fetchone()[0]


def get_trade_id(data):
    cursor.execute(f""" SELECT id FROM trades WHERE id = (select max(id) from trades) 
        AND customer_id = {data['customer_id']} AND seller_id = {data['seller_id']} AND coin = {data['coin']} 
        AND amount = {data['amount']} AND desc = '{data['desc']}' """)

    return cursor.fetchone()


def get_trade_data(trade_id):
    cursor.execute(f""" SELECT * FROM trades WHERE id = {trade_id} """)
    trade_data = cursor.fetchall()

    trade = {}
    count = 0

    if trade_data:
        for item in trade_items:
            trade[item] = trade_data[0][count]
            count += 1

    else:
        trade = None

    return trade


def delete_trade(trade_id):
    cursor.execute(f""" DELETE FROM trades WHERE id = {trade_id} """)
    connect.commit()


def trade_refused(trade_id):
    cursor.execute(f""" UPDATE trades SET status = 1 WHERE id = {trade_id} """)

    cursor.execute(f""" SELECT customer_id, coin, amount FROM trades WHERE id = {trade_id} """)
    trade_data = cursor.fetchall()

    cursor.execute(f""" SELECT {config.CURRENCY[trade_data[0][1]] + '_balance'} FROM users
                        WHERE id = {trade_data[0][0]} """)

    cursor.execute(f""" UPDATE users SET {config.CURRENCY[trade_data[0][1]] + '_balance'} =
                        {(Decimal("{:.2f}".format(float(cursor.fetchone()[0]))) +
                          Decimal("{:.2f}".format(float(trade_data[0][2]))))} WHERE id = {trade_data[0][0]} """)
    connect.commit()


def trade_confirmed(trade_id):
    cursor.execute(f""" UPDATE trades SET status = 2 WHERE id = {trade_id} """)
    connect.commit()


def get_trade_userid(trade_id, user):
    cursor.execute(f""" SELECT {user + '_id'} FROM trades WHERE id = {trade_id} """)
    cursor.execute(f""" SELECT userid FROM users WHERE id = {cursor.fetchone()[0]} """)

    return cursor.fetchone()[0]


def get_trade_status(trade_id):
    cursor.execute(f""" SELECT status FROM trades WHERE id = {trade_id} """)
    result = cursor.fetchone()[0]

    return result


def get_trade_users(trade_id):
    cursor.execute(f""" SELECT customer_id, seller_id FROM trades WHERE id = {trade_id} """)
    result = cursor.fetchone()

    users = {
        trade_items[1]: result[0],
        trade_items[2]: result[1],
    }

    return users


def trade_close(trade_id):
    global new_balance

    trade_data = get_trade_data(trade_id)

    seller_data = get_user_data(user_id=trade_data['seller_id'])

    if trade_data['status'] == 2:
        cursor.execute(f""" UPDATE trades SET status = 3 WHERE id = {trade_id} """)

        if trade_data['coin'] == 0 or trade_data['coin'] == 1:
            new_balance = (Decimal("{:.2f}".format(float(seller_data[config.CURRENCY[trade_data['coin']] + "_balance"])
                                                   + float(trade_data['amount']))))

        elif trade_data['coin'] == 2:
            new_balance = (Decimal("{:.8f}".format(float(seller_data['btc_balance']) + (float(trade_data['amount'])))))

        cursor.execute(f""" UPDATE users SET {config.CURRENCY[trade_data['coin']] + "_balance"} = {new_balance} 
                            WHERE userid = {seller_data['userid']} """)

        connect.commit()


def add_feedback(trade_id, customer_id, seller_id, feedback):
    cursor.execute(f""" INSERT INTO feedbacks (trade_id, customer_id, seller_id, feedback, date) VALUES (
                                                {trade_id}, {customer_id}, {seller_id}, '{feedback}', '{date}') """)
    connect.commit()


def open_dispute(trade_id, userid, reason):
    trade_data = get_trade_data(trade_id)
    dispute_user = ["customer_id", "seller_id"] if trade_data['customer_id'] == get_user_id(userid) \
        else ["seller_id", "customer_id"]

    cursor.execute(f""" SELECT * FROM disputes WHERE trade_id = {trade_id} """)

    if cursor.fetchone() is None:
        cursor.execute(f""" UPDATE trades SET status = 4 WHERE id = {trade_data['id']} """)

        cursor.execute(f""" INSERT INTO disputes (trade_id, who_open_id, who_for_id, reason, status, date) VALUES (
                        {trade_data['id']}, {trade_data[dispute_user[0]]}, {trade_data[dispute_user[1]]}, '{reason}',
                            '0', '{date}')""")

        connect.commit()


def get_dispute_data(trade_id):
    cursor.execute(f""" SELECT * FROM disputes WHERE trade_id = {trade_id} """)
    data = cursor.fetchall()

    dispute_data = {}
    count = 0

    if data:
        for item in dispute_items:
            dispute_data[item] = data[0][count]
            count += 1

    else:
        dispute_data = None

    return dispute_data


def get_trade_ids(userid, user_act, status, page=1):
    user_act_dict = {
        0: f"customer_id = {get_user_id(userid)} AND status = {status}",
        1: f"seller_id = {get_user_id(userid)} AND status = {status}"
    }

    cursor.execute(f""" SELECT id FROM trades WHERE {user_act_dict[user_act]} 
                        ORDER BY ID DESC LIMIT {(page - 1) * 6}, 6""")

    return cursor.fetchall()


def number_trades(userid, user_act, status):
    user_act_dict = {
        0: f"customer_id = {get_user_id(userid)} AND status = {status}",
        1: f"seller_id = {get_user_id(userid)} AND status = {status}"
    }

    cursor.execute(f""" SELECT COUNT(*) FROM trades WHERE {user_act_dict[user_act]} """)
    return cursor.fetchone()[0]


def number_closed_trades(userid):
    cursor.execute(f""" SELECT COUNT(*) FROM trades WHERE customer_id = {get_user_id(userid)} AND status = 3 """)
    number_buy = cursor.fetchone()[0]

    cursor.execute(f""" SELECT COUNT(*) FROM trades WHERE seller_id = {get_user_id(userid)} AND status = 3 """)
    number_sell = cursor.fetchone()[0]

    return number_buy, number_sell


def get_trade_feedback(trade_id):
    cursor.execute(f""" SELECT feedback FROM feedbacks WHERE trade_id = {trade_id} """)
    result = cursor.fetchone()

    if result is not None:
        return result[0]

    return None


add_tables()
