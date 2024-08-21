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
    username : Mapped[str] = mapped_column(db.String(255),nullable=False,unique=True)
    password : Mapped[str] = mapped_column(db.String(255),nullable=False)
    # role_id: Mapped[int] = mapped_column(db.Integer,db.ForeignKey('Roles.id'),nullable=False)

    role: Mapped['Role'] = db.relationship("Role")
    orders: Mapped[List["Order"]] = db.relationship(back_populates="customer",cascade="all, delete-orphan")

    role_id : Mapped[int] = mapped_column(db.ForeignKey('Roles.id'))
    
    customeraccount : Mapped["CustomerAccount"] = db.relationship("CustomerAccount", back_populates="customer", uselist=False)