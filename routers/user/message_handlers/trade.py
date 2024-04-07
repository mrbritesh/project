from decimal import Decimal
from aiogram import Router, types
from aiogram.fsm.context import FSMContext

import app
import config

from data import db
from words.user import trade_word
from keyboards.user import inline
from routers.func import antispam, remove_html_tags
from routers.user.message_handlers.main import message_handler_basefilter, message_handler_funcfilter
from state.state import FormTrade, FormFeedback, FormDismute

router = Router()


@router.message(FormTrade.seller_id)
async def seller_find(msg: types.Message, state: FSMContext):
    if await antispam(msg=msg):
        try:
            if msg.text.isdigit():
                if msg.from_user.id == int(msg.text):
                    bot_message = await msg.answer(trade_word.cannot_open_trade_yourself)
                    await del_old_message(msg.from_user.id, state)
                    await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                          state=state)

                else:
                    seller_data = db.get_user_data(userid=msg.text)

                    if seller_data is None:
                        bot_message = await msg.answer(trade_word.seller_not_found)
                        await del_old_message(msg.from_user.id, state)
                        await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                              state=state)

                    elif seller_data['userid'] == int(msg.text):
                        await state.update_data(seller_id=seller_data['id'])
                        pp = await app.bot.get_user_profile_photos(msg.text, limit=1)

                        if pp.photos:
                            await msg.answer_photo(pp.photos[-1][0].file_id, trade_word.seller_profile(seller_data),
                                                   reply_markup=inline.trade())

                        else:
                            await msg.answer(trade_word.seller_profile(seller_data), reply_markup=inline.trade())

                        await del_old_message(msg.from_user.id, state)
                        await state.set_state(FormTrade.status)

            elif msg.text[0] == "@":
                if msg.from_user.username == msg.text[1:]:
                    bot_message = await msg.answer(trade_word.cannot_open_trade_yourself)
                    await del_old_message(msg.from_user.id, state)
                    await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                          state=state)

                else:
                    seller_data = db.get_user_data(username=msg.text)

                    if seller_data is None:
                        bot_message = await msg.answer(trade_word.seller_not_found)
                        await del_old_message(msg.from_user.id, state)
                        await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                              state=state)

                    elif seller_data['username'] == msg.text.lower():
                        await state.update_data(seller_id=seller_data['id'])
                        pp = await app.bot.get_user_profile_photos(seller_data['userid'], limit=1)

                        if pp.photos:
                            await msg.answer_photo(pp.photos[-1][0].file_id, trade_word.seller_profile(seller_data),
                                                   reply_markup=inline.trade())

                        else:
                            await msg.answer(trade_word.seller_profile(seller_data), reply_markup=inline.trade())

                        await del_old_message(msg.from_user.id, state)
                        await state.set_state(FormTrade.status)

            else:
                if await message_handler_funcfilter(msg, state) is False:
                    bot_message = await msg.answer(trade_word.wrong_id_or_name)
                    await del_old_message(msg.from_user.id, state)
                    await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                          state=state)

        except:
            await msg.answer(trade_word.error_delete_message)


@router.message(FormTrade.coin)
async def chose_coin(msg: types.Message, state: FSMContext):
    if await antispam(msg=msg):
        try:
            data = await state.get_data()

            if data['status'] != 1:
                await message_handler_funcfilter(msg, state)

            else:
                await msg.delete()

        except:
            await msg.answer(trade_word.error_delete_message)


@router.message(FormTrade.amount)
async def amount(msg: types.Message, state: FSMContext):
    if await antispam(msg=msg):
        try:
            data = await state.get_data()
            user = db.get_user_data(userid=msg.from_user.id)

            if msg.text.find(",") > 0:
                bot_message = await msg.answer(trade_word.wrong_input_amount)
                await del_old_message(msg.from_user.id, state)
                await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                      state=state)

            elif data['coin'] == 0 or data['coin'] == 1:
                if msg.text.isdigit() or msg.text < "{:.3f}".format(float(msg.text)):
                    if (Decimal("{:.2f}".format(float(msg.text))) >
                            Decimal("{:.2f}".format(float(user[config.CURRENCY[data['coin']] + '_balance'])))):
                        bot_message = await msg.answer(trade_word.not_enough_money)
                        await del_old_message(msg.from_user.id, state)
                        await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                              state=state)

                    elif Decimal("{:.2f}".format(float(msg.text))) < config.TRADE_LIMIT_CURRENCY_AMOUNT[data['coin']]:
                        bot_message = await msg.answer(trade_word.trade_min_amount(data['coin']))
                        await del_old_message(msg.from_user.id, state)
                        await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                              state=state)

                    elif Decimal("{:.2f}".format(float(msg.text))) >= float(
                            config.TRADE_LIMIT_CURRENCY_AMOUNT[data['coin']]):
                        await state.update_data(amount="{:.2f}".format(float(msg.text)))
                        await msg.answer(trade_word.trade_desc, reply_markup=inline.desc())
                        await del_old_message(msg.from_user.id, state)
                        await save_message_id(amount_user_message_id=msg.message_id, state=state)
                        await state.set_state(FormTrade.desc)

                else:
                    bot_message = await msg.answer(trade_word.wrong_amount(data['coin']))
                    await del_old_message(msg.from_user.id, state)
                    await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                          state=state)

            elif data['coin'] == 2:
                if msg.text.isdigit() or msg.text < "{:.9f}".format(float(msg.text)):
                    if (Decimal("{:.8f}".format(float(msg.text))) >
                            Decimal("{:.8f}".format(float(user[config.CURRENCY[data['coin']] + '_balance'])))):
                        bot_message = await msg.answer(trade_word.not_enough_money)
                        await del_old_message(msg.from_user.id, state)
                        await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                              state=state)

                    elif Decimal("{:.8f}".format(float(msg.text))) < Decimal(
                            config.TRADE_LIMIT_CURRENCY_AMOUNT[data['coin']]):
                        bot_message = await msg.answer(trade_word.trade_min_amount(data['coin']))
                        await del_old_message(msg.from_user.id, state)
                        await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                              state=state)

                    elif Decimal("{:.8f}".format(float(msg.text))) >= float(
                            config.TRADE_LIMIT_CURRENCY_AMOUNT[data['coin']]):
                        await state.update_data(amount="{:.8f}".format(float(msg.text)))
                        await msg.answer(trade_word.trade_desc, reply_markup=inline.desc())
                        await del_old_message(msg.from_user.id, state)
                        await save_message_id(amount_user_message_id=msg.message_id, state=state)
                        await state.set_state(FormTrade.desc)

                else:
                    bot_message = await msg.answer(trade_word.wrong_amount(data['coin']))
                    await del_old_message(msg.from_user.id, state)
                    await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                          state=state)

        except:
            await msg.answer(trade_word.error_delete_message)


@router.message(FormTrade.desc)
async def trade_desc(msg: types.Message, state: FSMContext):
    if await antispam(msg=msg):
        try:
            if msg.text.isdigit() is False:
                if message_handler_basefilter(msg.text) or msg.text[0] == "/":
                    await msg.delete()

                else:
                    if len(msg.text) < 10:
                        bot_message = await msg.answer(trade_word.min_trade_desc)
                        await del_old_message(msg.from_user.id, state)
                        await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                              state=state)

                    else:
                        data = await state.get_data()
                        await state.update_data(desc=remove_html_tags(msg.text))
                        await msg.answer(trade_word.confirm_trade(data, remove_html_tags(msg.text)),
                                         reply_markup=inline.confirm_trade())
                        await del_old_message(msg.from_user.id, state)
                        await state.set_state(FormTrade.confirm)

        except:
            await msg.answer(trade_word.error_delete_message)


@router.message(FormTrade.confirm)
async def confirm_trade(msg: types.Message):
    if await antispam(msg=msg):
        await msg.delete()


@router.message(FormFeedback.feedback)
async def feedback(msg: types.Message, state: FSMContext):
    if await antispam(msg=msg):
        try:
            if message_handler_basefilter(msg.text) or msg.text[0] == "/":
                await msg.delete()

            else:
                if len(msg.text) < 5:
                    bot_message = await msg.answer(trade_word.not_enough_feedback)
                    await del_old_message(msg.from_user.id, state)
                    await save_message_id(bot_message_id=bot_message.message_id, user_message_id=msg.message_id,
                                          state=state)

                else:
                    data = await state.get_data()
                    await state.clear()
                    db.trade_close(data['trade_id'])
                    db.add_feedback(data['trade_id'], data['customer_id'], data['seller_id'], remove_html_tags(msg.text))
                    await msg.answer(trade_word.show_trade_data(data['trade_id'], 1, userid=msg.from_user.id))
                    await app.bot.send_message(db.get_userid(data['seller_id']),
                                               trade_word.show_trade_data(data['trade_id'], 1,
                                                                          userid=db.get_userid(data['seller_id'])))
                    await app.bot.send_message(config.CHAT_SERVICE_ID, trade_word.show_trade_data(data['trade_id'], 2))

        except:
            await msg.answer(trade_word.error_delete_message)


@router.message(FormDismute.input)
async def dispute(msg: types.Message, state: FSMContext):
    if await antispam(msg=msg):
        try:
            data = await state.get_data()

            if msg.text.isdigit() is False:
                if message_handler_basefilter(msg.text) or msg.text[0] == "/":
                    await msg.delete()

                elif len(msg.text) < 10:
                    if data.get("bot_message_id") and data.get("user_message_id"):
                        bot_message = await msg.answer(trade_word.not_enough_dismute)
                        await app.bot.delete_message(msg.from_user.id, data['bot_message_id'])
                        await app.bot.delete_message(msg.from_user.id, data['user_message_id'])
                        await state.update_data(
                            bot_message_id=bot_message.message_id,
                            user_message_id=msg.message_id,
                        )

                    else:
                        bot_message = await msg.answer(trade_word.not_enough_dismute)
                        await state.update_data(
                            bot_message_id=bot_message.message_id,
                            user_message_id=msg.message_id,
                        )

                else:
                    db.open_dispute(data['trade_id'], msg.from_user.id, msg.text)
                    dispute_data = db.get_dispute_data(data['trade_id'])
                    await msg.answer(trade_word.open_dismute)
                    await msg.answer(trade_word.show_trade_data(data['trade_id'], 0, userid=msg.from_user.id),
                                     reply_markup=inline.show_trade_data(data['trade_id']))
                    await app.bot.send_message(db.get_userid(dispute_data['who_for_id']),
                                               trade_word.show_trade_data(data['trade_id'], 0,
                                                                          userid=db.get_userid(dispute_data['who_for_id'])),
                                               reply_markup=inline.show_trade_data(data['trade_id']))
                    await state.clear()

                    if data.get("bot_message_id") and data.get("user_message_id"):
                        await app.bot.delete_message(msg.from_user.id, data['bot_message_id'])
                        await app.bot.delete_message(msg.from_user.id, data['user_message_id'])

        except:
            await msg.answer(trade_word.error_delete_message)


async def save_message_id(bot_message_id=None, user_message_id=None, coin_bot_message_id=None,
                          amount_user_message_id=None, state=None):
    if coin_bot_message_id is not None:
        await state.update_data(
            coin_bot_message_id=coin_bot_message_id,
        )

    elif amount_user_message_id is not None:
        await state.update_data(
            amount_user_message_id=amount_user_message_id,
        )

    elif bot_message_id is not None and user_message_id is not None:
        await state.update_data(
            bot_message_id=bot_message_id,
            user_message_id=user_message_id,
        )


async def del_old_message(userid, state, action=None):
    data = await state.get_data()

    if action is None:
        if data.get("bot_message_id") and data.get("user_message_id"):
            await app.bot.delete_message(userid, data['bot_message_id'])
            await app.bot.delete_message(userid, data['user_message_id'])
            await state.update_data(
                bot_message_id=None,
                user_message_id=None,
            )

    elif action == 0:
        if (data.get("bot_message_id") and data.get("user_message_id") and data.get("coin_bot_message_id") and
                data.get("amount_user_message_id")):
            await app.bot.delete_message(userid, data['bot_message_id'])
            await app.bot.delete_message(userid, data['user_message_id'])
            await app.bot.delete_message(userid, data['coin_bot_message_id'])
            await app.bot.delete_message(userid, data['amount_user_message_id'])
            await state.update_data(
                bot_message_id=None,
                user_message_id=None,
                coin_bot_message_id=None,
                amount_user_message_id=None,
            )

        elif (data.get("bot_message_id") is None and data.get("user_message_id") is None
              and data.get("coin_bot_message_id") and data.get("amount_user_message_id")):
            await app.bot.delete_message(userid, data['coin_bot_message_id'])
            await app.bot.delete_message(userid, data['amount_user_message_id'])
            await state.update_data(
                coin_bot_message_id=None,
                amount_user_message_id=None,
            )
