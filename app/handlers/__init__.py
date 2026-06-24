from aiogram import Router

from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
from .start import router as start_router
from .transactions import router as transactions_router


router = Router()

included_routers = (
    start_router,
    main_menu_router,
    navigation_router,
    transactions_router,
)
for included_router in included_routers:
    router.include_router(included_router)