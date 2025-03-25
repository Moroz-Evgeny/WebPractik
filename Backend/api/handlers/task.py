from typing import Union
from uuid import UUID

from fastapi import APIRouter, Request, Response, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import TaskCreate

from api.utils.jwt import _get_current_user_from_token
from api.utils.task import _get_team_id_by_teamlid_id, _create_new_task

from db.session import get_db
from db.dals import UserDAL
from db.models import PortalRole, User

task_router = APIRouter()

@task_router.post('/', response_model=Union[UUID, None])
async def create_new_task(task: TaskCreate, user: User = Depends(_get_current_user_from_token), session: AsyncSession = Depends(get_db)):
  if user.roles[0] == PortalRole.ROLE_PORTAL_USER:
    raise HTTPException(status_code=403, detail="Forbidden.")
  team_id = await _get_team_id_by_teamlid_id(id=user.user_id, session=session)
  if team_id is None:
    raise HTTPException(status_code=404, detail=f"The user:'{user.user_id}' team was not found.")
  try:
    return await _create_new_task(
      task=task,
      team_id=team_id,
      session=session,
    )
  except:
    raise HTTPException(status_code=503, detail=f"Database error.")