import logging
import sys
import asyncio

from app import dp, bot
from routers.func import update_rubusd_rate, update_btcusd_rate


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(update_rubusd_rate())
    loop.create_task(update_btcusd_rate())
    loop.create_task(main())
    loop.run_forever()
