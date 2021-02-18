import database.db as db
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

class User(db.Base):
    __tablename__ = 'users'

    ADMIN = '1'
    USER = '2'

    id = Column('id', String(15), primary_key=True, nullable=False)
    name = Column('name', String(50), primary_key=False, nullable=True)
    lastname = Column('lastname', String(50), primary_key=False, nullable=True)
    type = Column('type', String(1), server_default='2', nullable=False)
    items = relationship('Item', back_populates='users')
    orders = relationship('Order', back_populates='users')

    def __init__(self, id, type='2'):
        self.id = id
        self.type = type
    
    def __repr__(self):
        return f"<User {self.id}>"