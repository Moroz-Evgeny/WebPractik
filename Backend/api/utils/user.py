from typing import Union
from uuid import UUID

from fastapi import HTTPException, status
from api.schemas import UserCreate, ShowUser, UpdateUserRequest

from db.dals import UserDAL
from db.models import PortalRole, User

from hasher import Hasher

async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password),
            roles=[body.role],
        )
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            role=user.roles[0],
            is_active=user.is_active,
            invite_id=user.invite_id,
        )

async def _delete_user(id: UUID, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        remote_user_id = await user_dal.delete_user(id=id)
        if remote_user_id is not None:
            return remote_user_id

async def _update_user(id: UUID, update_user_params: dict, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        update_user_id = await user_dal.update_user(id=id, update_user_params=update_user_params)
        if update_user_id is not None:
            return update_user_id

async def _get_user_by_id(id: UUID, session) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(id=id)
        if user is not None:
            return user

async def _check_user_permissions(target_user: User, current_user: User) -> bool:
    if PortalRole.ROLE_PORTAL_SUPERADMIN in target_user.roles and PortalRole.ROLE_PORTAL_USER in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Superadmin cannot be deleted by the user."
        )
    if target_user.user_id != current_user.user_id:
        if PortalRole.ROLE_PORTAL_SUPERADMIN not in current_user.roles:
            return False
        if PortalRole.ROLE_PORTAL_SUPERADMIN in target_user.roles and PortalRole.ROLE_PORTAL_SUPERADMIN in current_user.roles:
            return False
    return True
