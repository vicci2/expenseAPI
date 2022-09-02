from fastapi import APIRouter
from .user import user_router
from .expenses import expenses_router

router = APIRouter()

router.include_router(user_router,prefix="/user",tags=["USERS"])
router.include_router(expenses_router,prefix="/expenses",tags=["EXPENSES"])