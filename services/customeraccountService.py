from database import db
from models.customer import Customer 
from models.customeraccount import CustomerAccount
from models.order import Order
from sqlalchemy import select
from utils.util import encode_token
from sqlalchemy.orm import joinedload

def save(customeraccount_data):
    customer = Customer.query.get(customeraccount_data['customer_id'])
    if not customer:
        return {"error": "Customer with the given ID does not exist"}, 400
    
    new_customeraccnt = CustomerAccount(
        password = customeraccount_data['password'],
        username = customeraccount_data['username'],
        customer_id = customeraccount_data['customer_id']
    )

    db.session.add(new_customeraccnt)
    db.session.commit()
    db.session.refresh(new_customeraccnt)
    return new_customeraccnt 

def find_all():
    query = select(CustomerAccount)
    all_customeraccnts = db.session.execute(query).scalars().all()
    return all_customeraccnts

def delete_customeraccnt(id):
    query = select(CustomerAccount).options(joinedload(CustomerAccount.customer)).where(CustomerAccount.id == id)
    customeraccnt=db.session.execute(query).scalar()

    if customeraccnt:
        db.session.delete(customeraccnt)
        db.session.commit()
        return customeraccnt
    else:
        return None

def update_customeraccnt(id,data):
    try:
        query = select(CustomerAccount).where(CustomerAccount.id == id)
        customer=db.session.execute(query).scalar()

        customer.username = data.get("username",customer.username)
        customer.password = data.get("password", customer.password)
        customer.customer_id = data.get("customer_id",customer.customer_id)
        
        db.session.commit()
        db.session.refresh(customer)
        return customer 
    except:
        return None
