from logging import getLogger
from typing import Union
from uuid import UUID

from fastapi import APIRouter, Request, Response
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import ShowUser, UserCreate, UpdateUserRequest
from api.utils import _create_new_user, _delete_user, _get_user_by_id, _update_user

from db.session import get_db
from db.dals import UserDAL
from db.models import PortalRole

user_router = APIRouter()
logger = getLogger(__name__)


@user_router.post("/", response_model=ShowUser)
async def create_new_user(body: UserCreate, session: AsyncSession = Depends(get_db)) -> ShowUser:
  try:
      return await _create_new_user(body, session=session)
  except IntegrityError as err:
    logger.error(err)
    raise HTTPException(status_code=503, detail=f"Database error: {err}")
  
@user_router.delete("/", response_model = Union[UUID, None])
async def delete_user_by_id(id: UUID, session: AsyncSession = Depends(get_db)) -> Union[UUID, None]:
    #Проверка на наличие юзера в бд
    user_to_delete = await _get_user_by_id(id=id,session=session)
    #Происходит удаление, если возвращается None, значит у пользователся флаг is_active = False
    delete_user_id = await _delete_user(id=id, session=session)
    if user_to_delete is None or delete_user_id is None:
       raise HTTPException(status_code=404, detail=f"User with id '{id}' is not found")      
    return delete_user_id

@user_router.patch("/", response_model = Union[UUID, None])
async def update_user_by_id(id: UUID, body: UpdateUserRequest, session: AsyncSession = Depends(get_db)) -> Union[UUID, None]:

   update_user_params = body.dict(exclude_none=True)
   if update_user_params == {}:
      raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")
   user_to_update = await _get_user_by_id(id=id, session=session)
   update_user_id = await _update_user(id=id, update_user_params=update_user_params, session=session)
   if user_to_update is None or update_user_id is None:
      raise HTTPException(status_code=404, detail=f"User with id '{id}' is not found") 
   return update_user_id