from typing import Union
from uuid import UUID

from fastapi import HTTPException, status
from api.schemas import TaskCreate

from db.dals import UserDAL
from db.models import PortalRole, User, Task

async def _get_team_id_by_teamlid_id(id: UUID, session) -> Union[UUID, None]:
  async with session.begin():
    user_dal = UserDAL(session)
    team_id = await user_dal.get_team_id_by_teamlid_id(id=id)
    if team_id is not None:
      return team_id

async def _create_new_task(task: TaskCreate, team_id: UUID, session) -> Union[None, UUID]:
  async with session.begin():
    user_dal = UserDAL(session)
    task_id = await user_dal.create_new_task(
      team_id=team_id,
      title=task.title,
      description=task.description,
      status=task.status,
      responsible=task.responsible,
    )
    if task_id is not None:
      return task_id