from aiogram import Router

from .main import router as main
from .trade import router as trade

router = Router()

router.include_routers(
    trade,
    main
)
