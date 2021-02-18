import database.db as db
from sqlalchemy import Table, Column, Integer, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship


class OrderItem(db.Base):
    __tablename__ = 'order_items'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    item_id = Column('item_id', String(15), ForeignKey('items.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    order_id = Column('order_id', String(15), ForeignKey('orders.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    quantity = Column('quantity', Integer, server_default='1', nullable=False)

    order = relationship("Order", back_populates="items")
    item = relationship("Item", back_populates="orderItems")

    #orders = relationship("Order", back_populates="items")
    when = Column('when', DateTime, server_default=func.now(), nullable=True)

    def __init__(self, item_id, order_id, quantity):
        self.item_id = item_id
        self.order_id = order_id
        self.quantity = quantity
    
    def __repr__(self):
        return f"<OrderItem {self.id}>"