from pydantic import BaseModel


class TodoGet(BaseModel):
    '''Класс отображения задач.'''
    title: str
    description: str

    class Config:
        orm_mode = True


class TodoCreate(BaseModel):
    '''Класс для создания задач.'''
    title: str
    description: str
