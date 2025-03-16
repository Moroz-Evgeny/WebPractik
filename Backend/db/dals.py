from typing import Union
from uuid import UUID
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import PortalRole, User


class UserDAL:
  def __init__(self, db_session: AsyncSession):
    self.db_session = db_session
  
  async def create_user(
      self,
      name: str,
      surname: str,
      email: str,
      hashed_password: str,
      roles: list[PortalRole],
      ) -> User:
    new_user = User(
      name=name,
      surname=surname,
      email=email,
      hashed_password=hashed_password,
      roles=roles,
    )
    self.db_session.add(new_user)
    await self.db_session.flush()
    return new_user
  
  async def delete_user(self, id: UUID) -> Union[UUID, None]:
    query = update(User).where(and_(User.user_id == id, User.is_active == True)).values(is_active = False).returning(User.user_id)
    result = await self.db_session.execute(query)
    remote_user_id = result.fetchone()
    if remote_user_id is not None:
      return remote_user_id[0]
  
  async def update_user(self, id: UUID, update_user_params: dict) -> Union[UUID, None]:
    query = update(User).where(and_(User.user_id == id, User.is_active == True)).values(update_user_params).returning(User.user_id)
    result = await self.db_session.execute(query)
    update_user_id = result.fetchone()
    if update_user_id is not None:
      return update_user_id[0]

  async def get_user_by_id(self, id: UUID) -> Union[User, None]:
    query = select(User).where(User.user_id == id)
    result = await self.db_session.execute(query)
    user_row = result.fetchone()
    if user_row is not None:
      return user_row[0]