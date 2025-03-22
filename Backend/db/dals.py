from typing import Union
from uuid import UUID
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import PortalRole, User, Team, UserAndTeam, Task

import uuid

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
    invite_id = str(uuid.uuid4())[:8]
    if roles[0] == PortalRole.ROLE_PORTAL_TEAMLID:
      invite_id = None
    new_user = User(
      user_id=uuid.uuid4(),
      name=name,
      surname=surname,
      email=email,
      hashed_password=hashed_password,
      roles=roles,
      invite_id=invite_id,
    )
    if roles[0] == PortalRole.ROLE_PORTAL_TEAMLID:
      new_team = Team(
        team_id=uuid.uuid4(),
        teamlid_id=new_user.user_id,
      )
      team_id=new_team.team_id
      self.db_session.add(new_team)
    else:
      team_id=None

    user_and_team = UserAndTeam(
      user_id=new_user.user_id,
      team_id=team_id,
      )  
    self.db_session.add(user_and_team)  
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
  
  async def get_user_by_email(self, email: str) -> Union[None, User]:
    query = select(User).where(User.email == email)
    result = await self.db_session.execute(query)
    user_row = result.fetchone()
    if user_row is not None:
      return user_row[0]
  
  async def get_team_id_by_teamlid_id(self, id: UUID) -> Union[None, UUID]:
    query = select(Team).where(Team.teamlid_id == id)
    result = await self.db_session.execute(query)
    team_row = result.fetchone()
    if team_row is not None:
      return team_row[0].team_id
  
  async def create_new_task(
      self,
      team_id: str,
      title: str,
      description: str,
      status: str,
      responsible: str) -> Union[None, UUID]:
    new_task = Task(
      team_id=team_id,
      title=title,
      description=description,
      status=status,
      responsible=responsible,
    )
    self.db_session.add(new_task)
    self.db_session.flush()
    return new_task.task_id