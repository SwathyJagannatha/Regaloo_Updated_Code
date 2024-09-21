from database import db
from models.customer import Customer 
from models.customeraccount import CustomerAccount
from models.role import Role
from models.order import Order
from sqlalchemy import select
from utils.util import encode_token
from sqlalchemy.orm import joinedload
from werkzeug.security import check_password_hash
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def login(username,password): #login using unique info so we dont query mutiple users
    query = select(CustomerAccount).where(CustomerAccount.username == username)
    customeraccnt = db.session.execute(query).scalar_one_or_none()
    #query cust table for a customer with password and username

    cust_id = customeraccnt.customer_id
    query1 = select(Customer).where(Customer.id == cust_id)
    customer = db.session.execute(query1).scalar_one_or_none()

    print("customerid",cust_id)
    print("customername",customer.name)
    if customeraccnt and customeraccnt.password == password:
      
        auth_token = encode_token(customeraccnt.id,customeraccnt.role.role_name)

        response = {
            "status": "success",
            "message" : "Successfully Logged In",
            "auth_token" : auth_token,
            "customer_id" :cust_id,
            "name":customer.name,
            "custaccount_id": customeraccnt.id
        }
        return response,True
    
    else:
        response = {
            "status" : "fail",
            "message" : "Invalid username or password"
        }
        return response,False

def masked_password(password):
    return '*' * len(password)
    
def logout():
    pass

def signup(custaccount_data):
    result = create_custaccnt(custaccount_data)
    return result,201

def save(customeraccount_data):
    cust_id = customeraccount_data.get('customer_id')
    username =customeraccount_data.get('username')
    password = customeraccount_data.get('password')
    role_id = customeraccount_data.get('role_id', 1)

    # query = select(CustomerAccount).where(CustomerAccount.customer_id == cust_id)
    # customer=db.session.execute(query).scalar_one_or_none()

    customer_query = select(Customer).where(Customer.id == cust_id)
    customer = db.session.execute(customer_query).scalar_one_or_none()
    
    if customer is None:
        return {
            "status":"fail",
            "message": "Customer not found"
            },404
    
    find_user = db.session.execute(select(CustomerAccount).where(CustomerAccount.username == username)).scalar()

    if find_user:
        return {"Message: CustomerAccount with that username already exists"},400
    
    new_customeraccnt = CustomerAccount(
        username=username,
        password=password,
        customer_id=cust_id,
        role_id=role_id
    )
    try:
        db.session.add(new_customeraccnt)
        db.session.commit()
        db.session.refresh(new_customeraccnt)

        return new_customeraccnt,201

    except Exception as e:
        return {"Message: CustomerAccount creation failed!"},404

def create_custaccnt(customeraccnt_data):
    customer_id = customeraccnt_data.get('customer_id')
    username =  customeraccnt_data.get('username')
    password = customeraccnt_data.get('password')
    role_id = customeraccnt_data.get('role_id')

    query = select(Customer).where(Customer.id == customer_id)
    customer=db.session.execute(query).scalar_one_or_none()

    if customer is None:
        return {
            "status":"fail",
            "message": "Customer not found"
            },404
    
    query = select(CustomerAccount).where(CustomerAccount.username == username)
    username_info=db.session.execute(query).scalar_one_or_none()

    if username_info:
        return {
            "status":"fail",
            "message": "Username already exists in our system"
            },404
    
    query = select(Role).where(Role.id == role_id)
    role=db.session.execute(query).scalar_one_or_none()

    if not role:
        return {
            "status":"fail",
            "message": "Provided role doesnt exist"
            },404
    
    new_customeraccnt = CustomerAccount(
        password = password,
        username = username,
        customer_id = customer_id,
        role_id = role_id
    )
    try:
        db.session.add(new_customeraccnt)
        db.session.commit()
        db.session.refresh(new_customeraccnt)
        return new_customeraccnt,201
    
    except Exception as e:
        return{
            "status":"fail",
            "message": f"Customer account creation failed {str(e)}"
        }

def find_all():
    query = select(CustomerAccount)
    all_customeraccnts = db.session.execute(query).scalars().all()
    logging.debug(f"Retrieved {len(all_customeraccnts)} customer accounts")
    
    if not all_customeraccnts:
        return {"Message": "Could not find customer accounts"}, 404
    
    return all_customeraccnts, 201

def get_account_by_id(id):
  try:
    query = select(CustomerAccount).where(CustomerAccount.id == id)
    customeraccnt = db.session.execute(query).scalar()

    if not customeraccnt:
        return {"Message: Customer Account was not found!!"},404   
    return customeraccnt,201
  
  except Exception as e:
    return {"Message:Could not find customer with this id"},404
  
def delete_customeraccnt(id):
    query = select(CustomerAccount).options(joinedload(CustomerAccount.customer)).where(CustomerAccount.id == id)
    customeraccnt=db.session.execute(query).scalar()

    if customeraccnt:
        db.session.delete(customeraccnt)
        db.session.commit()
        return customeraccnt,201
    else:
        return {"Message: Could not find out customeraccount with the specific id"},404

def update_customeraccnt(id,data):
    try:
        query = select(CustomerAccount).where(CustomerAccount.id == id)
        customer=db.session.execute(query).scalar()

        if not customer:
            return {"Message: Customer with the specified id doesnt exist"},404

        customer.username = data.get("username",customer.username)
        customer.password = data.get("password", customer.password)
        customer.customer_id = data.get("customer_id",customer.customer_id)
        
        db.session.commit()
        db.session.refresh(customer)
        return customer 
    except:
        return None
