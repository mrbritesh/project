import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from words.user import button_word
from data import db


def trade():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_trade[0], callback_data="s_fbs"),
            InlineKeyboardButton(text=button_word.inline_trade[1], callback_data="str_trd")
        ]]
    )

    return markup


def paginator_seller_feedback(seller_id, page=1):
    number_feedbacks = db.number_user_feedback(seller_id)
    total_page = math.ceil(number_feedbacks / 5)

    if number_feedbacks:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=button_word.inline_paginator[1], callback_data="prv_s_fdb_pg"),
                InlineKeyboardButton(text=f"{page}/{total_page}", callback_data="None"),
                InlineKeyboardButton(text=button_word.inline_paginator[0], callback_data="nxt_s_fdb_pg")
            ], [
                InlineKeyboardButton(text=button_word.inline_back[0], callback_data="bk_s_pf")
            ]]
        )

    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text=button_word.inline_back[0], callback_data="bk_s_pf")
            ]]
        )

    return markup


def coin():
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_coin[0], callback_data="rub"),
            InlineKeyboardButton(text=button_word.inline_coin[1], callback_data="usd"),
            InlineKeyboardButton(text=button_word.inline_coin[2], callback_data="btc")
        ], [
            InlineKeyboardButton(text=button_word.inline_cancel[0], callback_data="cl_trd")
        ]]
    )

    return markup


def amount():
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_back[0], callback_data="bk_cn")
        ]]
    )

    return markup


def desc():
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_cancel[0], callback_data="cl_trd"),
            InlineKeyboardButton(text=button_word.inline_back[0], callback_data="bk_amt")
        ]]
    )

    return markup


def confirm_trade():
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_cancel[0], callback_data="cl_trd"),
            InlineKeyboardButton(text=button_word.inline_confirm[0], callback_data="cfm_trd")
        ]]
    )

    return markup


def confirm_trade_seller(trade_id):
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_confirm_trade_seller[0], callback_data=f"s_rf_trd_id#{trade_id}"),
            InlineKeyboardButton(text=button_word.inline_confirm_trade_seller[1], callback_data=f"s_cf_trd_id#{trade_id}")
        ]]
    )

    return markup


def show_trade_data(trade_id):
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_info_trade[0], callback_data=f"sw_trd_dt_id#{trade_id}")
        ]]
    )

    return markup


def trade_option(trade_id, ua=None):
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_open_dismute[0], callback_data=f"opn_dm_id#{trade_id}"),
        ], [
            InlineKeyboardButton(text=button_word.inline_close_trade[0], callback_data=f"trd_cs_id#{trade_id}")
        ]]
    )

    if ua == 0:
        markup.inline_keyboard.append([InlineKeyboardButton(text=button_word.inline_back[0],
                                                            callback_data=f"bk_actv_trd_ua&{ua}")])

    return markup


def decide_trade(trade_id):
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_yes_no[1], callback_data=f"n_trd_cs_id#{trade_id}"),
            InlineKeyboardButton(text=button_word.inline_yes_no[0], callback_data=f"y_trd_cs_id#{trade_id}")
        ]]
    )

    return markup


def open_dismute(trade_id, ua=None):
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_open_dismute[0], callback_data=f"opn_dm_id#{trade_id}")
        ]]
    )

    if ua == 1:
        markup.inline_keyboard.append([InlineKeyboardButton(text=button_word.inline_back[0],
                                                            callback_data=f"bk_actv_trd_ua&{ua}")])

    return markup


def back_trade_option():
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_back[0], callback_data=f"bk_trd_optn")
        ]]
    )

    return markup


def without_feedback():
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_without_feedback[0], callback_data="wth_fb")
        ]]
    )

    return markup


def optional():
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_optional[0], url="t.me/@snakeweb")
        ], [
            InlineKeyboardButton(text=button_word.inline_optional[1], callback_data="faq")
        ]]
    )

    return markup


def trade_frozen_instruction():
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_trade_frozen_instruction[0], url="t.me/@snakeweb")
        ]]
    )

    return markup


def all_trades():
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_all_trade[0], callback_data="actv_trds")
        ], [
            InlineKeyboardButton(text=button_word.inline_all_trade[1], callback_data="hstr_trds")
        ]]
    )

    return markup


def type_trade(action):
    type_trade_dict = {
        0: "actv_trd",
        1: "hstr_trd"
    }

    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_type_trade[0], callback_data=f"{type_trade_dict[action]}_buy"),
            InlineKeyboardButton(text=button_word.inline_type_trade[1], callback_data=f"{type_trade_dict[action]}_sell")
        ], [
            InlineKeyboardButton(text=button_word.inline_back[0], callback_data="bk_all_trds")
        ]]
    )

    return markup


def back_history_trades(ua):
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_back[0], callback_data=f"bk_hstr_trd_ua&{ua}")
        ]]
    )

    return markup


def paginator_trades(userid, number_trades, ua, status, page=1):
    status_dict = {
        2: f"actv_trd_{'buy' if ua == 0 else 'sell'}",
        3: f"hstr_trd_{'buy' if ua == 0 else 'sell'}"
    }

    paginator_dict = {
        2: [f"prv_actv_trd_ua&{ua}_p&{page}", f"nxt_actv_trd_ua&{ua}_p&{page}"],
        3: [f"prv_hstr_trd_ua&{ua}_p&{page}", f"nxt_hstr_trd_ua&{ua}_p&{page}"],
        "back": f"bk_{'actv_trd' if status == 2 else 'hstr_trd'}"
    }

    if number_trades:
        total_page = math.ceil(number_trades / 5)
        prefixes = db.get_trade_ids(userid, ua, status, page)

        rows = []
        row = 0
        count = 0

        for prefix in prefixes:
            if count == 1:
                rows[row].append(InlineKeyboardButton(text=button_word.inline_paginator_active_trades(prefix[0]),
                                                      callback_data=f"{status_dict[status]}_id#{prefix[0]}"))
                row += 1
                count = 0

            else:
                rows.append([InlineKeyboardButton(text=button_word.inline_paginator_active_trades(prefix[0]),
                                                  callback_data=f"{status_dict[status]}_id#{prefix[0]}")])
                count += 1

        rows.append([InlineKeyboardButton(text=button_word.inline_paginator[1], callback_data=paginator_dict[status][0]),
                     InlineKeyboardButton(text=f"{page}/{total_page}", callback_data="None"),
                     InlineKeyboardButton(text=button_word.inline_paginator[0], callback_data=paginator_dict[status][1])])

        rows.append([InlineKeyboardButton(text=button_word.inline_back[0], callback_data=paginator_dict['back'])])

        markup = InlineKeyboardMarkup(inline_keyboard=rows)

    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text=button_word.inline_back[0], callback_data=paginator_dict['back'])
            ]]
        )

    return markup


def faq():
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=button_word.inline_faq[0], url="t.me/@snakeweb")
        ], [
            InlineKeyboardButton(text=button_word.inline_faq[1], url="t.me/@snakeweb")
        ], [
            InlineKeyboardButton(text=button_word.inline_back[0], callback_data="bk_optl")
        ]]
    )

    return markup


def support():
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=button_word.inline_back[0], callback_data="bk_optl")
        ]]
    )

    return markup
