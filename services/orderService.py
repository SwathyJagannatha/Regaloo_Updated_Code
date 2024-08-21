from models.order import Order
from models.product import Product
from models.customer import Customer
from database import db
from sqlalchemy import select
from datetime import date
from sqlalchemy.orm import joinedload

def save(order_data):
    new_order = Order(date=date.today(), customer_id=order_data["customer_id"])

    # Process each product in the order_data
    for product in order_data.get('products', []):
        product_id = product.get('id')
        if not product_id:
            continue  # Skip if no product ID is provided

        # Query for the product
        query = select(Product).filter(Product.id == product_id)
        item = db.session.execute(query).scalar()
        if item:
            new_order.products.append(item)
        else:
            print(f"Product with ID {product_id} not found")

    db.session.add(new_order)
    db.session.commit()
    db.session.refresh(new_order)
    return new_order

def find_all():
    query = select(Order)
    all_orders = db.session.execute(query).scalars().all()
    return all_orders

def find_by_id(id):
    query = select(Order).where(Order.id == id)
    order = db.session.execute(query).scalars().all()
    return order


def find_by_customer_id(id):
    query = select(Order).where(Order.customer_id == id)
    orders = db.session.execute(query).scalars().all()
    return orders

def find_by_customer_email(email):
    query = select(Order).join(Customer).where(Customer.id == Order.customer_id).filter(Customer.email == email)
    orders = db.session.execute(query).scalars().all()
    return orders

def delete_order(id):
    #query = select(Order).where(Order.id == id)
    query = select(Order).options(joinedload(Order.customer)).where(Order.id == id)
    order = db.session.execute(query).scalar_one_or_none()

    if order:
        db.session.delete(order)
        db.session.commit()
        return order
    else:
        return None

def update_order(id,data):
    try:
        query = select(Order).where(Order.id == id)
        order=db.session.execute(query).scalar()

        order.date = data.get("date",order.date)
        order.customer_id = data.get("customer_id",order.customer_id)
        db.session.commit()
        return order 
    except:
        return None