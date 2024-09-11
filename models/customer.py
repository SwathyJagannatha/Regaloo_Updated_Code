from database import db,Base
from sqlalchemy.orm import Mapped,mapped_column
from typing import List
from models.role import Role

class Customer(Base):
    __tablename__='Customers'
    id : Mapped[int] = mapped_column(primary_key = True)
    name : Mapped[str] = mapped_column(db.String(255),nullable=False)
    email : Mapped[str] = mapped_column(db.String(255),nullable=False,unique=True)
    phone : Mapped[str] = mapped_column(db.String(255),nullable=False)
    
    customeraccount : Mapped["CustomerAccount"] = db.relationship("CustomerAccount", back_populates="customer", uselist=False)