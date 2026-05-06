from aiogram import Router

from .type import router as type_router
from .amount import router as amount_router
from .category import router as category_router
from .account import router as account_router
from .description import router as description_router


router = Router()

router.include_router(type_router)
router.include_router(amount_router)
router.include_router(category_router)
router.include_router(account_router)
router.include_router(description_router)