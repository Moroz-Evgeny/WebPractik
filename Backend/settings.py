from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
  "REAL_DATABASE_URL",
  default="postgresql+asyncpg://postgres:postgres@db:5432/"
)