from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import app

from data import db
from keyboards.user import inline
from words.user import button_word, main
from state.state import FormTrade
from routers.func import antispam

router = Router()


@router.message(F.text == button_word.reply_user_menu[0])
async def search_seller(msg: types.Message, state: FSMContext):
    user = db.get_user_data(userid=msg.from_user.id)

    if user is not None:
        if await antispam(msg=msg):
            db.add_user(userid=msg.from_user.id, fullname=msg.from_user.full_name, username=msg.from_user.username)
            user_id = db.get_user_id(msg.from_user.id)
            await state.update_data(
                customer_id=user_id
            )
            await msg.answer(main.search_seller)
            await state.set_state(FormTrade.seller_id)


@router.message(F.text == button_word.reply_user_menu[1])
async def profile(msg: types.Message):
    user = db.get_user_data(userid=msg.from_user.id)

    if user is not None:
        if await antispam(msg=msg):
            db.add_user(userid=msg.from_user.id, fullname=msg.from_user.full_name, username=msg.from_user.username)
            pp = await app.bot.get_user_profile_photos(msg.from_user.id)

            if pp.photos:
                await msg.answer_photo(pp.photos[-1][0].file_id, main.profile(msg.from_user.id))

            else:
                await msg.answer(main.profile(msg.from_user.id))


@router.message(F.text == button_word.reply_user_menu[2])
async def all_trades(msg: types.Message):
    user = db.get_user_data(userid=msg.from_user.id)

    if user is not None:
        if await antispam(msg=msg):
            db.add_user(userid=msg.from_user.id, fullname=msg.from_user.full_name, username=msg.from_user.username)
            await msg.answer(main.all_trades, reply_markup=inline.all_trades())


@router.message(F.text == button_word.reply_user_menu[3])
async def optional(msg: types.Message):
    user = db.get_user_data(userid=msg.from_user.id)

    if user is not None:
        if await antispam(msg=msg):
            db.add_user(userid=msg.from_user.id, fullname=msg.from_user.full_name, username=msg.from_user.username)
            await msg.answer(main.optional, reply_markup=inline.optional())


def message_handler_basefilter(message):
    prefixes = [button_word.reply_user_menu[0], button_word.reply_user_menu[1], button_word.reply_user_menu[2],
                button_word.reply_user_menu[3]]

    return any(prefix == message for prefix in prefixes)


async def message_handler_funcfilter(msg, state):
    prefixes = [button_word.reply_user_menu[0], button_word.reply_user_menu[1], button_word.reply_user_menu[2],
                button_word.reply_user_menu[3]]

    if msg.text == button_word.reply_user_menu[0]:
        await search_seller(msg, state)

    elif msg.text == button_word.reply_user_menu[1]:
        await profile(msg)
        await state.clear()

    elif msg.text == button_word.reply_user_menu[2]:
        await all_trades(msg)
        await state.clear()

    elif msg.text == button_word.reply_user_menu[3]:
        await optional(msg)
        await state.clear()

    return any(prefix == msg.text for prefix in prefixes)
