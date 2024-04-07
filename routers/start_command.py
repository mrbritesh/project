import os

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app

from data import db
from words.user import main
from keyboards.user import reply
from state.state import FormCaptcha
from routers.func import antispam, remove_html_tags, create_captcha

router = Router()


@router.message(CommandStart())
async def start_command(msg: types.Message, state: FSMContext):
    if msg.chat.type == "private":
        if msg.from_user.username is not None:
            user = db.get_user_data(userid=msg.from_user.id)

            if await antispam(msg=msg):
                if user is None:
                    captcha = create_captcha(msg.from_user.id)
                    bot_message = await msg.answer_photo(types.FSInputFile(captcha[1]), main.captcha)
                    await state.update_data(
                        image=bot_message.message_id,
                        code=captcha[0],
                    )
                    await state.set_state(FormCaptcha.input)
                    os.remove(captcha[1])

                elif user['ban'] != 1:
                    db.add_user(msg.from_user.id, remove_html_tags(msg.from_user.full_name), msg.from_user.username)
                    await msg.answer(main.welcome, reply_markup=reply.user_menu())

        else:
            await msg.answer(main.none_username)


@router.message(FormCaptcha.input)
async def captcha_checker(msg: types.Message, state: FSMContext):
    if await antispam(msg=msg):
        try:
            if msg.text.isdigit():
                data = await state.get_data()

                if msg.text != data['code']:
                    captcha = create_captcha(msg.from_user.id)
                    bot_message = await msg.answer_photo(types.FSInputFile(captcha[1]), main.captcha)
                    await msg.delete()
                    await app.bot.delete_message(msg.from_user.id, data['image'])
                    await state.update_data(
                        image=bot_message.message_id,
                        code=captcha[0],
                    )
                    os.remove(captcha[1])

                else:
                    await msg.delete()
                    await app.bot.delete_message(msg.from_user.id, data['image'])
                    await state.clear()
                    db.add_user(msg.from_user.id, remove_html_tags(msg.from_user.full_name), msg.from_user.username)
                    await msg.answer(main.welcome, reply_markup=reply.user_menu())

            else:
                await msg.delete()

        except:
            await msg.delete()
