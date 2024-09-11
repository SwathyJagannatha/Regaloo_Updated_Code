from models.product import Product
from models.orderProduct import order_product
from database import db
from sqlalchemy import select,delete

def save(product_data):
    new_product = Product(name = product_data["name"], price = product_data["price"],description = product_data["description"],stock_qty = product_data["stock_qty"])
    db.session.add(new_product)
    db.session.commit()
    db.session.refresh(new_product)
    return new_product

def find_all():
    query = select(Product)
    all_products = db.session.execute(query).scalars().all()
    return all_products

def search_product(search_term):
    query = select(Product).where(Product.name.like(f'%{search_term}%'))
    search_products = db.session.execute(query).scalars().all()
    return search_products

def delete_product(id):
    query = select(Product).where(Product.id == id)
    prod = db.session.execute(query).scalar()

    if prod:
        # Delete all associations from the order_product table where product_id matches
        db.session.execute(
            delete(order_product).where(order_product.c.product_id == id)
        )

        db.session.delete(prod)
        db.session.commit()
        return prod,201
    else:
        return {"Message":"Product deletion failed"},404
    
def update_product(id,data):
    try:
        query = select(Product).where(Product.id == id)
        prod = db.session.execute(query).scalar()
        prod.name = data.get("name",prod.name)
        prod.price = data.get("price",prod.price)

        db.session.commit()
        return prod
    except:
        return None
    




    
