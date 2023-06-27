from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Todo(Base):
    '''Класс задач.'''
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False, doc='Описание задачи')
    owner_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'),
                      doc='Автор задачи')
    owner = relationship('User', back_populates='todo')
