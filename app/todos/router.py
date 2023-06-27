from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from todos.models import Todo
from todos.shemas import TodoCreate, TodoGet
from users.base_config import current_user

router = APIRouter(
    prefix='/todo',
    tags=['Todo list']
)


@router.get('', response_model=List[TodoGet])
async def get_all_todo(current_user=Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    try:
        user_id = current_user.id
        query = select(Todo).filter(Todo.owner_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                'status': 'error',
                'data': 'Произошла ошибочка',
                'details': None
            }
        )


@router.get('/{title}', response_model=TodoGet)
async def get_one_todo(title: str, current_user=Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    query = select(Todo).where(Todo.title == title)
    try:
        result = await session.execute(query)
        final_res = result.scalars().first()
        if (final_res.owner_id != current_user.id
                and current_user.is_superuser is False):
            raise HTTPException(
                status_code=403,
                detail={
                    'status': 'error',
                    'data': ('Вы не можете просматривать '
                             'запись чужого пользователя'),
                    'detail': None}
            )
        return final_res
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': ('Такой записи не существует '
                     'или произошла ошибка на сервере'),
            'details': None
        })


@router.post('')
async def create_todo(todo: TodoCreate, current_user=Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Todo).values(**todo.dict(), owner_id=current_user.id)
        await session.execute(stmt)
        await session.commit()
        return {
            'status': 'Todo added successfully!'
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                'status': 'error',
                'data': 'Произошла ошибка - запись не добавлена!',
                'details': None
            }
        )


@router.put('/{title}')
async def update_todo(title: str, todo: TodoCreate,
                      current_user=Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    try:
        user_id = current_user.id
        await get_one_todo(title=title,
                           current_user=current_user,
                           session=session)
        stmt = update(Todo).where(Todo.title == title).values(**todo.dict(),
                                                              owner_id=user_id)
        await session.execute(stmt)
        await session.commit()
        return {
            'status': 'Todo successfully updated!'
            }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                'status': 'error',
                'data': 'Такой записи нет или вы не можете ее изменять',
                'details': None
            }
            )


@router.delete('/{title}')
async def delete_todo(title: str,  current_user=Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    try:
        await get_one_todo(title=title,
                           current_user=current_user,
                           session=session)
        stmt = delete(Todo).where(Todo.title == title)
        await session.execute(stmt)
        await session.commit()
        return {
            'status': 'Delete succes!'
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                'status': 'error',
                'data': 'Такой записи нет или вы не можете ее удалить',
                'details': None
                }
            )
