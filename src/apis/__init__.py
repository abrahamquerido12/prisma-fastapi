from fastapi import APIRouter

from src.apis.auth import router as authRouter
from src.apis.users import router as usersRouter
from src.apis.oficios import router as oficiosRouter

apis = APIRouter()
apis.include_router(authRouter)
apis.include_router(usersRouter)

apis.include_router(oficiosRouter)

__all__ = ["apis"]
