from fastapi import FastAPI
from fastapi.routing import APIRouter

from api.user_handlers import user_router
from api.login_handlers import login_router

import uvicorn

app = FastAPI(title='WebPractik')

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=['user'])
main_api_router.include_router(login_router, prefix="/login", tags=['login'])

app.include_router(main_api_router)

if __name__ == "__main__":
  uvicorn.run("main:app", host="localhost", port=8000, reload=True, access_log=True)