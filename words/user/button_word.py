# Reply button words
reply_user_menu = [
    "🔍 Поиск пользователя",
    "👤 Мой профиль",
    "📁 Все сделки",
    "🛎 Дополнительно",
]

# Inline button words
inline_sub_channel = [
    "Channel #1",
    "Channel #2",
    "🔄 Проверить",
]

inline_profile = [
    "➕ Пополнить",
    "➖ Вывести",
]

inline_trade = [
    "💬 Отзывы",
    "🛒 Начать сделку"
]

inline_back = [
    "⬅️ Назад"
]

inline_paginator = [
    "➡️",
    "⬅️"
]

inline_coin = [
    "RUB",
    "USD",
    "BTC"
]

inline_cancel = [
    "⛔️ Отменить"
]

inline_confirm = [
    "✅ Подтвердить"
]

inline_confirm_trade_seller = [
    "⛔️ Отказать",
    "✅ Принять"
]

inline_info_trade = [
    "📂 Информация сделки"
]

inline_close_trade = [
    "✅ Завершить сделку"
]

inline_open_dismute = [
    "🔏 Открыть спор"
]

inline_yes_no = [
    "Да",
    "Нет"
]

inline_without_feedback = [
    "➡️ Пропустить"
]

inline_optional = [
    "🧑🏻‍💻 Поддержка",
    "💬 FAQ"
]

inline_trade_frozen_instruction = [
    "🔗 Инструкция"
]

inline_faq = [
    "Как пользоваться ботом?",
    "Как закрыт спор?"
]

inline_all_trade = [
    "⏳ Активные сделки",
    "⌛️ История сделок"
]

inline_type_trade = [
    "🛒 Покупок",
    "📦 Продаж"
]


def inline_paginator_active_trades(trade_id):
    text = f"Сделка №: {trade_id}"
    return text
