from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from users.base_config import fastapi_users
from users.models import User
from users.shemas import AdminCreate, UserRead
from users.utils_admin import check_superuser

router = APIRouter(
    prefix='/admin_rout',
    tags=['User auth for admin']
)


router.include_router(
    fastapi_users.get_register_router(UserRead, AdminCreate),
    prefix="/add_user",
    dependencies=[Depends(check_superuser)]
)


@router.delete('/delete/{username}')
async def delete_user(username: str, current_user=Depends(check_superuser),
                      session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = delete(User).where(User.username == username)
        await session.execute(stmt)
        await session.commit()
        return {
            'status': f'User - {username} deleted successfully!'
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                'status': 'error',
                'data': 'Произошла ошибочка',
                'details': None
            })
