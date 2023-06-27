from fastapi import FastAPI

from todos.router import router as router_todo
from users.base_config import auth_backend, fastapi_users
from users.router import router as router_admin
from users.shemas import UserCreate, UserRead

app = FastAPI(
    title='TODOs',
    description='TODO API на FASTAPI'
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
    responses={
        204: 'Login succes'
    }
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_todo)
app.include_router(router_admin)
