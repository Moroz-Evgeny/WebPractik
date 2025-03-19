from typing import Union

from hasher import Hasher

from db.dals import UserDAL
from db.models import User


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