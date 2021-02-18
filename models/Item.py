import database.db as db
from sqlalchemy import Table, Column, Integer, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class Item(db.Base):
    __tablename__ = 'items'

    ITEM_INACTIVE = 0
    ITEM_ACTIVE = 1

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(50), server_default='0', nullable=False)
    description = Column('description', String(100), server_default='0', nullable=False)
    value = Column('value', Float, server_default='0', nullable=False)
    status = Column('type', Integer, server_default='0', nullable=False)

    orderItems = relationship('OrderItem', back_populates='item')

    user_id = Column('user_id', String(15), ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    users = relationship("User", back_populates="items")


    #order_id = Column('order_id', String(15), ForeignKey('orders.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    #orders = relationship("Order", back_populates="items")

    def __init__(self, name, value, status, user_id):
        self.name = name
        self.value = value
        self.status = status 
        self.user_id = user_id
    
    def __repr__(self):
        return f"<Item {self.id}>"