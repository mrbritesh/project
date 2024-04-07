import math

from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

import app
import config

from data import db
from keyboards.user import inline
from routers.func import antispam
from routers.user.callback_queries.main import callback_query_basefilter, callback_query_funcfilter
from routers.user.message_handlers.trade import save_message_id, del_old_message
from state.state import FormTrade, FormFeedback, FormDismute
from words.user import trade_word

router = Router()


@router.callback_query(FormTrade.status)
async def seller_found(call: types.CallbackQuery, state: FSMContext):
    if await antispam(call=call):
        data = await state.get_data()
        seller_data = db.get_user_data(user_id=data['seller_id'])

        if call.data == "bk_s_pf":
            await state.update_data(paginator_page=1)
            await call.message.delete()
            pp = await app.bot.get_user_profile_photos(seller_data['userid'], limit=1)

            if pp.photos:
                await call.message.answer_photo(pp.photos[-1][0].file_id, trade_word.seller_profile(seller_data),
                                                reply_markup=inline.trade())

            else:
                await call.message.answer(trade_word.seller_profile(seller_data), reply_markup=inline.trade())

        elif call.data == "str_trd":
            bot_message = await app.bot.send_message(call.from_user.id, trade_word.choose_coin, reply_markup=inline.coin())
            await state.update_data(status=1)
            await save_message_id(coin_bot_message_id=bot_message.message_id, state=state)
            await state.set_state(FormTrade.coin)

        elif call.data == "s_fbs":
            await state.update_data(paginator_page=1)
            await call.message.delete()
            await call.message.answer(trade_word.seller_feedbacks(data['seller_id']),
                                      reply_markup=inline.paginator_seller_feedback(data['seller_id']))

        elif call.data == "prv_s_fdb_pg" or call.data == "nxt_s_fdb_pg":
            try:
                global page

                if call.data == "prv_s_fdb_pg":
                    page = data['paginator_page'] - 1 if data['paginator_page'] > 1 else 1

                elif call.data == "nxt_s_fdb_pg":
                    page = data['paginator_page'] + 1 if data['paginator_page'] < math.ceil(
                        db.number_user_feedback(data['seller_id']) / 5) else data['paginator_page']

                await state.update_data(paginator_page=page)
                await call.message.edit_text(trade_word.seller_feedbacks(seller_data['id'], page),
                                             reply_markup=inline.paginator_seller_feedback(seller_data['id'], page))

            except TelegramBadRequest:
                await call.answer(trade_word.empty_page, cache_time=60, show_alert=True)

        else:
            await callback_query_funcfilter(call)


@router.callback_query(FormTrade.coin)
async def coin(call: types.CallbackQuery, state: FSMContext):
    if await antispam(call=call):
        if call.data == "usd" or call.data == "rub" or call.data == "btc":
            await state.update_data(coin=config.CURRENCY_ID[call.data])
            await call.message.edit_text(
                trade_word.amount(userid=call.from_user.id, coin=config.CURRENCY_ID[call.data]),
                reply_markup=inline.amount())
            await state.set_state(FormTrade.amount)

        else:
            await cancel_trade(call, state)


@router.callback_query(FormTrade.amount)
async def amount(call: types.CallbackQuery, state: FSMContext):
    if await antispam(call=call):
        data = await state.get_data()
        if call.data == "bk_cn":
            if not data.get("amount"):
                await state.update_data(coin=None)
                await call.message.edit_text(trade_word.choose_coin, reply_markup=inline.coin())
                await del_old_message(call.from_user.id, state)
                await state.set_state(FormTrade.coin)


@router.callback_query(FormTrade.desc)
async def trade_desc(call: types.CallbackQuery, state: FSMContext):
    if await antispam(call=call):
        data = await state.get_data()
        if call.data == "bk_amt":
            if not data.get("desc"):
                await state.update_data(amount=None)
                bot_message = await call.message.edit_text(trade_word.amount(call.from_user.id, data['coin']),
                                                           reply_markup=inline.amount())
                await del_old_message(call.from_user.id, state, action=0)
                await save_message_id(coin_bot_message_id=bot_message.message_id, state=state)
                await state.set_state(FormTrade.amount)

        else:
            await cancel_trade(call, state)


@router.callback_query(FormTrade.confirm)
async def confirm_trade(call: types.CallbackQuery, state: FSMContext):
    if await antispam(call=call):
        if call.data == "cfm_trd":
            data = await state.get_data()
            trade_id = db.add_trade(call.from_user.id, data)
            sellerid = db.get_userid(data['seller_id'])
            await call.message.edit_text(trade_word.waiting_confirm_trade_seller)
            await app.bot.send_message(sellerid, trade_word.confirm_trade_seller(data),
                                       reply_markup=inline.confirm_trade_seller(trade_id))
            await state.clear()

        else:
            await cancel_trade(call, state)


@router.callback_query(FormFeedback.feedback)
async def feedback(call: types.CallbackQuery, state: FSMContext):
    if await antispam(call=call):
        if call.data == "wth_fb":
            data = await state.get_data()
            db.trade_close(data['trade_id'])
            await call.message.edit_text(trade_word.show_trade_data(data['trade_id'], 1, userid=call.from_user.id))
            await app.bot.send_message(db.get_userid(data['seller_id']),
                                       trade_word.show_trade_data(data['trade_id'], 1,
                                                                  userid=db.get_userid(data['seller_id'])))
            await app.bot.send_message(config.CHAT_SERVICE_ID, trade_word.show_trade_data(data['trade_id'], 2))
            await state.clear()


@router.callback_query(FormDismute.input)
async def dismute(call: types.CallbackQuery, state: FSMContext):
    if await antispam(call=call):
        if call.data == "bk_trd_optn":
            data = await state.get_data()
            trade_user = db.get_trade_users(data['trade_id'])
            user_act = "customer" if trade_user["customer_id"] == db.get_user_id(call.from_user.id) else "seller"

            inline_func = {
                "customer": inline.trade_option(data['trade_id']),
                "seller": inline.open_dismute(data['trade_id']),
            }

            if data.get("bot_message_id") and data.get("user_message_id"):
                await app.bot.delete_message(call.from_user.id, data['bot_message_id'])
                await app.bot.delete_message(call.from_user.id, data['user_message_id'])
                await call.message.edit_text(
                    trade_word.show_trade_data(data['trade_id'], 1, userid=call.from_user.id),
                    reply_markup=inline_func[user_act])
                await state.clear()

            else:
                await call.message.edit_text(
                    trade_word.show_trade_data(data['trade_id'], 1, userid=call.from_user.id),
                    reply_markup=inline_func[user_act])
                await state.clear()


@router.callback_query(callback_query_basefilter(['s_cf_trd', 's_rf_trd', 'sw_trd_dt', 'trd_cs', 'y_trd_cs', 'n_trd_cs', 'opn_dm']))
async def sorting(call: types.CallbackQuery, state: FSMContext):
    if await antispam(call=call):
        func = {
            "s_cf_trd": [seller_confirm_trade, 0],
            "s_rf_trd": [seller_confirm_trade, 0],
            "sw_trd_dt": [show_trade_data, 0],
            "trd_cs": [decide_trade, 1],
            "y_trd_cs": [decide_trade, 1],
            "n_trd_cs": [decide_trade, 1],
            "opn_dm": [decide_trade, 1],
        }

        for prefix in func:
            if call.data.startswith(prefix):
                await func[prefix][0](call) if func[prefix][1] == 0 else await func[prefix][0](call, state)


async def seller_confirm_trade(call: types.CallbackQuery):
    if await antispam(call=call):
        customerid = db.get_trade_userid(call.data[call.data.index("#"):][1:], "customer")
        trade_status = db.get_trade_status(call.data[call.data.index("#"):][1:])

        if call.data.startswith("s_cf_trd") and trade_status == 0:
            db.trade_confirmed(call.data[call.data.index("#"):][1:])

            await call.message.edit_text(trade_word.show_trade_data(call.data[call.data.index("#"):][1:], 0),
                                         reply_markup=inline.show_trade_data(call.data[call.data.index("#"):][1:]))
            await app.bot.send_message(customerid,
                                       trade_word.show_trade_data(call.data[call.data.index("#"):][1:],
                                                                  0),
                                       reply_markup=inline.show_trade_data(
                                           call.data[call.data.index("#"):][1:]))

        elif call.data.startswith("s_rf_trd") and trade_status == 0:
            db.trade_refused(call.data[call.data.index("#"):][1:])

            await call.message.edit_text(trade_word.show_trade_data(call.data[call.data.index("#"):][1:], 0),
                                         reply_markup=inline.show_trade_data(call.data[call.data.index("#"):][1:]))
            await app.bot.send_message(customerid,
                                       trade_word.show_trade_data(call.data[call.data.index("#"):][1:], 0),
                                       reply_markup=inline.show_trade_data(call.data[call.data.index("#"):][1:]))


async def show_trade_data(call: types.CallbackQuery):
    if await antispam(call=call):
        trade_data = db.get_trade_data(call.data[call.data.index("#"):][1:])
        user_act = "customer" if trade_data["customer_id"] == db.get_user_id(call.from_user.id) else "seller"

        if trade_data['status'] == 1 or trade_data['status'] == 3 and user_act == "seller":
            await call.message.edit_text(trade_word.show_trade_data(trade_data['id'], 1, userid=call.from_user.id))

        elif trade_data['status'] == 2 and user_act == "customer":
            await call.message.edit_text(trade_word.show_trade_data(trade_data['id'], 1, userid=call.from_user.id),
                                         reply_markup=inline.trade_option(trade_data['id']))

        elif trade_data['status'] == 2 and user_act == "seller":
            await call.message.edit_text(trade_word.show_trade_data(trade_data['id'], 1, userid=call.from_user.id),
                                         reply_markup=inline.open_dismute(trade_data['id']))

        elif trade_data['status'] == 4:
            await call.message.edit_text(trade_word.show_trade_data(trade_data['id'], 1, userid=call.from_user.id),
                                         reply_markup=inline.trade_frozen_instruction())


async def decide_trade(call: types.CallbackQuery, state: FSMContext):
    if await antispam(call=call):
        trade_data = db.get_trade_data(call.data[call.data.index("#"):][1:])

        if call.data.startswith("trd_cs") and trade_data['status'] == 2:
            await call.message.edit_text(trade_word.trade_close, reply_markup=inline.decide_trade(trade_data['id']))

        elif call.data.startswith("y_trd_cs") and trade_data['status'] == 2:
            bot_message = await call.message.edit_text(trade_word.write_feedback,
                                                       reply_markup=inline.without_feedback())

            await state.update_data(
                bot_message_id=bot_message.message_id,
                trade_id=trade_data['id'],
                customer_id=trade_data['customer_id'],
                seller_id=trade_data['seller_id']
            )

            await state.set_state(FormFeedback.feedback)

        elif call.data.startswith("n_trd_cs") and trade_data['status'] == 2:
            await call.message.edit_text(trade_word.show_trade_data(trade_data['id'], 1, call.from_user.id),
                                         reply_markup=inline.trade_option(trade_data['id']))

        elif call.data.startswith("opn_dm") and trade_data['status'] == 2:
            bot_message = await call.message.edit_text(trade_word.dismute, reply_markup=inline.back_trade_option())

            await state.update_data(
                main_bot_message_id=bot_message.message_id,
                trade_id=trade_data['id']
            )

            await state.set_state(FormDismute.input)


async def cancel_trade(call: types.CallbackQuery, state: FSMContext):
    if await antispam(call=call):
        if call.data.startswith("cl_trd"):
            data = await state.get_data()

            if data.get("coin") is None:
                await state.set_state(FormTrade.status)
                await call.message.delete()

            else:
                await state.clear()
                await call.message.edit_text(trade_word.trade_canceled)
