from aiogram import Router

from .account import router as account_router
from .amount import router as amount_router
from .category import router as category_router
from .description import router as description_router
from .type import router as type_router

router = Router()

included_routers = (
    type_router,
    amount_router,
    category_router,
    account_router,
    description_router,
)
for included_router in included_routers:
    router.include_router(included_router)
