from enum import Enum
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import declarative_base

import uuid

Base = declarative_base()

class User(Base):
  __tablename__ = "users"

  user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = Column(String, nullable=False)
  surname = Column(String, nullable=False)
  email = Column(String, nullable=False, unique=True)
  is_active = Column(Boolean(), default=True)
  hashed_password = Column(String, nullable=False)
  roles = Column(ARRAY(String), nullable=False)
  invite_id = Column(String, nullable=True)

class UserAndTeam(Base):
   __tablename__ = "userandteam"

   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
   user_id = Column(UUID(as_uuid=True), nullable=False)
   team_id = Column(UUID(as_uuid=True), nullable=True, default=None) 

class Team(Base):
   __tablename__ = "teams"
  
   team_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   teamlid_id = Column(UUID(as_uuid=True), nullable=False)


class Task(Base):
   __tablename__ = "tasks"

   task_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   team_id = Column(UUID(as_uuid=True), nullable=False)
   title = Column(String, nullable=False)
   description = Column(String, nullable=False)
   status = Column(String, nullable=False)
   responsible = Column(String, nullable=False)


class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"
    ROLE_PORTAL_TEAMLID = "ROLE_PORTAL_TEAMLID"
    ROLE_PORTAL_SUPERADMIN = "ROLE_PORTAL_SUPERADMIN"
    