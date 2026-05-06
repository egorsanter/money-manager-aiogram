from aiogram import Router

from .main import router as main_router
from .navigation import router as navigation_router
from .start import router as start_router
from .transactions import router as transactions_router

router = Router()

router.include_router(main_router)
router.include_router(navigation_router)
router.include_router(start_router)
router.include_router(transactions_router)