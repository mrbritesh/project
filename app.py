import config

from routers import router
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=config.BOT_API, parse_mode="HTML", disable_web_page_preview=True)
dp = Dispatcher(storage=storage)

dp.include_router(router)
