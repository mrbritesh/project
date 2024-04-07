import math

from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest

from data import db
from routers.func import antispam
from words.user import main, trade_word
from keyboards.user import inline

router = Router()


def callback_query_basefilter(prefixes):
    async def predicate(call: types.CallbackQuery):
        return any(call.data.startswith(prefix) for prefix in prefixes)

    return predicate


async def callback_query_funcfilter(call):
    all_trade_prefixes = ['actv_trds', 'hstr_trds', 'actv_trd_buy', 'actv_trd_sell', 'hstr_trd_buy', 'hstr_trd_sell',
                          "bk_all_trds"]
    optional_prefixes = ['faq', 'bk_optl']

    if any(prefix == call.data for prefix in all_trade_prefixes):
        if call.data == "actv_trds" or call.data == "hstr_trds":
            await suitable_trade(call)

        elif call.data == "actv_trd_buy" or call.data == "actv_trd_sell":
            await active_trades(call)

        elif call.data == "hstr_trd_buy" or call.data == "hstr_trd_sell":
            await history_trades(call)

        elif call.data == "bk_all_trds":
            await back_all_trades(call)

    elif any(prefix == call.data for prefix in optional_prefixes):
        if call.data == "faq":
            await faq(call)

        elif call.data == "bk_optl":
            await back_optional(call)


@router.callback_query(callback_query_basefilter(['actv_trds', 'hstr_trds']))
async def suitable_trade(call: types.CallbackQuery):
    if await antispam(call=call):
        await call.message.edit_text(main.type_trade, reply_markup=inline.type_trade(0 if call.data == "actv_trds" else 1))


@router.callback_query(callback_query_basefilter(['actv_trd_buy', 'actv_trd_sell', 'prv_actv_trd', 'nxt_actv_trd', 'bk_actv_trd']))
async def active_trades(call: types.CallbackQuery):
    if await antispam(call=call):
        global page

        if call.data == "actv_trd_buy" or call.data == "actv_trd_sell":
            number_active_trades = db.number_trades(call.from_user.id, 0 if call.data == "actv_trd_buy" else 1, 2)
            await call.message.edit_text(
                main.paginator_trades(number_active_trades, 0 if call.data == "actv_trd_buy" else 1, 2),
                reply_markup=inline.paginator_trades(call.from_user.id, number_active_trades,
                                                     0 if call.data == "actv_trd_buy" else 1, 2))

        elif call.data[:12] == "actv_trd_buy":
            await call.message.edit_text(trade_word.show_trade_data(call.data[call.data.index("#"):][1:], 1,
                                                                    userid=call.from_user.id),
                                         reply_markup=inline.trade_option(call.data[call.data.index("#"):][1:], ua=0))

        elif call.data[:13] == "actv_trd_sell":
            await call.message.edit_text(trade_word.show_trade_data(call.data[call.data.index("#"):][1:], 1,
                                                                    userid=call.from_user.id),
                                         reply_markup=inline.open_dismute(call.data[call.data.index("#"):][1:], ua=1))

        elif call.data[:12] == "prv_actv_trd" or call.data[:12] == "nxt_actv_trd":
            try:
                number_active_trades = db.number_trades(call.from_user.id,
                                                        int(call.data[call.data.index("ua&"):call.data.index("_p&")][3:]),
                                                        2)

                if call.data[:12] == "prv_actv_trd":
                    page = int(call.data[call.data.index("p&"):][2:]) - 1 if int(call.data[call.data.index("p&"):][2:]) > 1 \
                        else 1

                elif call.data[:12] == "nxt_actv_trd":
                    page = int(call.data[call.data.index("p&"):][2:]) + 1 if (int(call.data[call.data.index("p&"):][2:]) <
                                                                              math.ceil(number_active_trades / 5)) \
                        else int(call.data[call.data.index("p&"):][2:])

                await call.message.edit_text(
                    main.paginator_trades(
                        number_active_trades, int(call.data[call.data.index("ua&"):call.data.index("_p&")][3:]), 2),
                    reply_markup=inline.paginator_trades(call.from_user.id, number_active_trades,
                                                         int(call.data[call.data.index("ua&"):call.data.index("_p&")][3:]),
                                                         2, page=page))

            except TelegramBadRequest:
                await call.answer(trade_word.empty_page, cache_time=60, show_alert=True)

        elif call.data == "bk_actv_trd":
            await call.message.edit_text(main.type_trade, reply_markup=inline.type_trade(0))

        elif call.data[:11] == "bk_actv_trd":
            number_active_trades = db.number_trades(call.from_user.id, int(call.data[call.data.index("ua&"):][3:]), 2)
            await call.message.edit_text(
                main.paginator_trades(number_active_trades, int(call.data[call.data.index("ua&"):][3:]), 2),
                reply_markup=inline.paginator_trades(call.from_user.id, number_active_trades,
                                                     int(call.data[call.data.index("ua&"):][3:]), 2))


@router.callback_query(callback_query_basefilter(['hstr_trd_buy', 'hstr_trd_sell', 'prv_hstr_trd', 'nxt_hstr_trd', 'bk_hstr_trd']))
async def history_trades(call: types.CallbackQuery):
    if await antispam(call=call):
        global page

        if call.data == "hstr_trd_buy" or call.data == "hstr_trd_sell":
            number_history_trades = db.number_trades(call.from_user.id, 0 if call.data == "hstr_trd_buy" else 1, 3)
            await call.message.edit_text(
                main.paginator_trades(number_history_trades, 0 if call.data == "hstr_trd_buy" else 1, 3),
                reply_markup=inline.paginator_trades(call.from_user.id, number_history_trades,
                                                     0 if call.data == "hstr_trd_buy" else 1, 3))

        elif call.data[:12] == "hstr_trd_buy" or call.data[:13] == "hstr_trd_sell":
            await call.message.edit_text(trade_word.show_trade_data(call.data[call.data.index("#"):][1:], 1,
                                                                    userid=call.from_user.id, hide=True),
                                         reply_markup=inline.back_history_trades(0 if call.data[:12] == "hstr_trd_buy" else 1))

        elif call.data[:12] == "prv_hstr_trd" or call.data[:12] == "nxt_hstr_trd":
            try:
                number_history_trades = db.number_trades(call.from_user.id,
                                                         int(call.data[call.data.index("ua&"):call.data.index("_p&")][3:]),
                                                         3)

                if call.data[:12] == "prv_hstr_trd":
                    page = int(call.data[call.data.index("p&"):][2:]) - 1 if int(call.data[call.data.index("p&"):][2:]) > 1 \
                        else 1

                elif call.data[:12] == "nxt_hstr_trd":
                    page = int(call.data[call.data.index("p&"):][2:]) + 1 if (int(call.data[call.data.index("p&"):][2:]) <
                                                                              math.ceil(
                                                                                  number_history_trades / 5)) else int(
                        call.data[call.data.index("p&"):][2:])

                await call.message.edit_text(
                    main.paginator_trades(number_history_trades,
                                          int(call.data[call.data.index("ua&"):call.data.index("_p&")][3:]), 3),
                    reply_markup=inline.paginator_trades(call.from_user.id, number_history_trades,
                                                         int(call.data[call.data.index("ua&"):call.data.index("_p&")][3:]),
                                                         3, page=page))

            except TelegramBadRequest:
                await call.answer(trade_word.empty_page, cache_time=60, show_alert=True)

        elif call.data == "bk_hstr_trd":
            await call.message.edit_text(main.type_trade, reply_markup=inline.type_trade(1))

        elif call.data[:11] == "bk_hstr_trd":
            number_history_trades = db.number_trades(call.from_user.id, int(call.data[call.data.index("ua&"):][3:]), 3)
            await call.message.edit_text(
                main.paginator_trades(number_history_trades, int(call.data[call.data.index("ua&"):][3:]), 3),
                reply_markup=inline.paginator_trades(call.from_user.id, number_history_trades,
                                                     int(call.data[call.data.index("ua&"):][3:]), 3))


@router.callback_query(F.data == "bk_all_trds")
async def back_all_trades(call: types.CallbackQuery):
    if await antispam(call=call):
        await call.message.edit_text(main.all_trades, reply_markup=inline.all_trades())


@router.callback_query(F.data == "faq")
async def faq(call: types.CallbackQuery):
    if await antispam(call=call):
        await call.message.edit_text(main.faq, reply_markup=inline.faq())


@router.callback_query(F.data == "bk_optl")
async def back_optional(call: types.CallbackQuery):
    if await antispam(call=call):
        await call.message.edit_text(main.optional, reply_markup=inline.optional())