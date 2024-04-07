from aiogram.filters.state import State, StatesGroup


class FormCaptcha(StatesGroup):
    image = State()
    code = State()
    input = State()


class FormTrade(StatesGroup):
    bot_message_id = State()
    user_message_id = State()
    coin_bot_message_id = State()
    amount_user_message_id = State()
    customer_id = State()
    seller_id = State()
    status = State()
    paginator_page = State()
    coin = State()
    amount = State()
    desc = State()
    confirm = State()


class FormFeedback(StatesGroup):
    bot_message_id = State()
    trade_id = State()
    customer_id = State()
    seller_id = State()
    feedback = State()


class FormDismute(StatesGroup):
    main_bot_message_id = State()
    bot_message_id = State()
    user_message_id = State()
    trade_id = State()
    input = State()
