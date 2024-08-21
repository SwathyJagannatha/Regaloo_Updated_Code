from database import db,Base
from sqlalchemy.orm import Mapped,mapped_column
from typing import List

class CustomerAccount(Base):
    __tablename__='CustomerAccount'
    id : Mapped[int] = mapped_column(primary_key = True)
    username : Mapped[str] = mapped_column(db.String(255),nullable=False,unique=True)
    password : Mapped[str] = mapped_column(db.String(255),nullable=False)
    customer_id : Mapped[int] = mapped_column(db.ForeignKey('Customers.id',ondelete='CASCADE'))
    
    customer : Mapped["Customer"] = db.relationship("Customer",back_populates="customeraccount")