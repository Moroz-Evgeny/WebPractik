import settings

from create_jwt import create_access_token, create_refresh_token

from datetime import timedelta

from db.session import get_db
from db.dals import UserDAL

from api.utils_for_user import _get_user_by_id
from api.utils_for_jwt import _authenticate_user
from api.schemas import Token

from typing import Union

from fastapi import APIRouter, Request, Response, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.ext.asyncio import AsyncSession

login_router = APIRouter()

@login_router.post('/', response_model=Token)
async def login_for_acess_token(
  response: Response,
  form_data: OAuth2PasswordRequestForm = Depends(),
  db: AsyncSession = Depends(get_db)) -> Token:
  user = await _authenticate_user(user_email=form_data.username, user_password=form_data.password, session=db)
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Incorrect username or password")
  
  access_token = create_access_token(
    data={"sub": str(user.user_id), "role": user.roles[0], "invite_id": user.invite_id, "team_id:": "..."}
  )
  refresh_token = create_refresh_token(
    data={"sub": str(user.user_id), "role": user.roles[0],}
  )

  response.set_cookie(
    key="refresh_token",
    value=refresh_token,
    httponly=True,  
    # secure=True,              # Только HTTPS
    samesite="strict", 
    max_age=60 * 60 * 24 * 7
  )
  return Token(access_token=access_token, token_type='bearer')