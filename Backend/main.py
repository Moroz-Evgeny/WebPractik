from fastapi import FastAPI
from fastapi.routing import APIRouter

from api.user_handlers import user_router

import uvicorn

app = FastAPI(title='WebPractik')

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user")

app.include_router(main_api_router)

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, access_log=True)