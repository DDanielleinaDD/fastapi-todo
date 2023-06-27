from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from users.base_config import current_user


async def check_superuser(current_user=Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail={
                'status': 'error',
                'data': 'У вас нет доступа к этому действию. '
                        'Только для админа!',
                'details': None
            })
