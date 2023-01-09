from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, utils, ws_test, rtc_test

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(ws_test.router, prefix="/ws_test", tags=["ws_test"])
api_router.include_router(rtc_test.router, prefix="/rtc_test", tags=["rtc_test"])
