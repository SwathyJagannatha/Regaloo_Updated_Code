from database import db,Base
from sqlalchemy.orm import Mapped,mapped_column
from models.orderProduct import order_product
# from models.product import Product
#from models.customer import Customer
from typing import List

class Order(Base):
    __tablename__='Orders'
    id : Mapped[int] = mapped_column(primary_key = True)
    date : Mapped[str] = mapped_column(db.Date,nullable=False)
    customer_id : Mapped[int] = mapped_column(db.ForeignKey('Customers.id',ondelete='CASCADE'))

    # Many to one : Order and customer

    customer : Mapped["Customer"] = db.relationship(back_populates="orders")

    # Many-to many : products with no back_populates

    # products : Mapped[List["Product"]] = db.relationship(secondary = order_product, lazy = 'noload')
    
    products : Mapped[List["Product"]] = db.relationship(secondary = order_product)
