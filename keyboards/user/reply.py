import words.user.button_word

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def user_menu():
    markup = ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text=words.user.button_word.reply_user_menu[0]),
        KeyboardButton(text=words.user.button_word.reply_user_menu[1])
    ], [
        KeyboardButton(text=words.user.button_word.reply_user_menu[2]),
        KeyboardButton(text=words.user.button_word.reply_user_menu[3])
    ]], resize_keyboard=True)

    return markup
