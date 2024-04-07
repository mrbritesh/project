from aiogram import Router

from .start_command import router as start_command_router
from .user import router as user_router

router = Router()

router.include_routers(
    user_router,
    start_command_router,
)
