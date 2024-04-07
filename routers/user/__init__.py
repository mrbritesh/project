from aiogram import Router

from .message_handlers import router as message_handler_router
from .callback_queries import router as callback_query_router

router = Router()

router.include_routers(
    callback_query_router,
    message_handler_router
)
