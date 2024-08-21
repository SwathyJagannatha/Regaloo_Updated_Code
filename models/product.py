from database import db,Base 
from sqlalchemy.orm import Mapped,mapped_column

class Product(Base):
    __tablename__ = "Products"
    id : Mapped[int] = mapped_column(primary_key = True)
    name : Mapped[str] = mapped_column(db.String(255))
    price : Mapped[float] = mapped_column(db.Float())