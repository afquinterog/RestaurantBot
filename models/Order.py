import database.db as db
from sqlalchemy import Table, Column, Integer, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship


class Order(db.Base):
    __tablename__ = 'orders'

    ORDER_BASKET = 0
    ORDER_DONE = 1
    ORDER_DELIVERED = 2

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    amount = Column('amount', Float, server_default='0', nullable=True)
    when = Column('when', DateTime, server_default=func.now(), nullable=True)
    status = Column('status', Integer, server_default='0', nullable=False)
    
    items = relationship('OrderItem', back_populates='order')

    user_id = Column('user_id', String(15), ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    users = relationship("User", back_populates="orders")


    def __init__(self, user_id, status=''):
        self.user_id = user_id
        self.status = status
    
    def __repr__(self):
        return f"<Order {self.id}>"