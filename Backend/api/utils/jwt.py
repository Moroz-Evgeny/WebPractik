import settings

from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from hasher import Hasher

from db.dals import UserDAL
from db.models import User
from db.session import get_db

from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from api.utils.user import _get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def _get_user_by_email_for_token(email: str, session) -> Union[None, User]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_email(email=email)
        if user is not None:
            return user

async def _authenticate_user(user_email: str, user_password: str, session) -> Union[None, User]:
    async with session.begin():
      user_dal = UserDAL(session)
      user = await user_dal.get_user_by_email(email=user_email)
      if user is None:
          return None
      if Hasher.verify_password(user_password, user.hashed_password) == False:
          return None
      return user

async def _get_current_user_from_token(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)) -> Union[User, None]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except:
        raise credentials_exception
    user = await _get_user_by_id(user_id, session)
    if user is None:
        raise credentials_exception
    return user
