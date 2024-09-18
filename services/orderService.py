from models.order import Order
from models.product import Product
from models.customer import Customer
from models.customeraccount import CustomerAccount
from models.orderProduct import order_product
from database import db
from sqlalchemy import select
from datetime import date,datetime
from sqlalchemy.orm import joinedload
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask import current_app,url_for,render_template,request,make_response 
from flask_mail import Message
from extensions import mail
from email.utils import make_msgid

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

def compare_products(prod1,prod2):
    if len(prod1) != len(prod2):
        return False 
    
    sorted_prod1 = sorted(prod1 , key = lambda x : x['id'])
    sorted_prod2 = sorted(prod2, key = lambda x : x['id'])

    for prod1,prod2 in zip(sorted_prod1,sorted_prod2):
        if prod1['id'] != prod2['id']:
            return False 
    return True 

def create_order(data):
    custaccount_id = data.get("customeraccnt_id")
    product_ids = data.get('products', [])

    # Fetch the CustomerAccount object
    custaccnt_id = select(CustomerAccount).where(CustomerAccount.id == custaccount_id)
    custaccnt_obj = db.session.execute(custaccnt_id).scalar_one_or_none()
    total_amt = 0

    if not custaccnt_obj:
        return {f"Message": f"CustomerAccount with id {custaccount_id} not found!!"}, 404 
    

    # check for duplicate orders 
    # check if order with customeraccntid already exists 

    existing_order = select(Order).where(Order.customeraccnt_id == custaccount_id)
    orders_obj = db.session.execute(existing_order).scalars().all()

    for order in orders_obj:
        existing_prods = [
            { "id" : prod.id , "quantity": prod.stock_qty, "description": prod.description}
            for prod in order.products
        ]

        if compare_products(existing_prods,product_ids):
            return {"Message": "Duplicate order found for same customer id with same product list"},404

    # List to hold Product objects
    prod_arr = []

    for prod in product_ids:
        prod_query = select(Product).where(Product.id == prod['id'])
        prod_obj = db.session.execute(prod_query).scalar_one_or_none()

        if not prod_obj:
            return {"Message": f"Product with id {prod['id']} not found!!"}, 404  
       
        total_amt += prod_obj.price
        prod_arr.append(prod_obj)

    # Create the Order object
    latest_order = Order(date=datetime.now(), customeraccnt_id=custaccount_id, total_amount=total_amt, status="Pending Order")

    # Append Product objects to the Order
    latest_order.products.extend(prod_arr)

    db.session.add(latest_order)
    db.session.commit()
    db.session.refresh(latest_order)

    #order_id and customeraccnt_id
    send_confirm_email(latest_order.customeraccnt_id,latest_order.id)

    return {
        "status": "success",
        "message": "Order placed successfully",
        "order_info": {
            "id": latest_order.id,
            "date": latest_order.date,
            "total_amount": latest_order.total_amount,
            "products": [{"id": p.id, "name": p.name, "price": p.price} for p in latest_order.products],
            "status": latest_order.status
        }
    }, 201


def send_confirm_email(custaccnt_id,order_id ):
    customeraccnt = CustomerAccount.query.get(custaccnt_id)
    customer_id = customeraccnt.customer_id

    customer = Customer.query.get(customer_id)
    print("Customer name",customer.name)
    print("Customer email",customer.email)

    s = Serializer(current_app.config['SECRET_KEY'])
    token = s.dumps({'custaccnt_id': custaccnt_id,'order_id':order_id,'msg_id': message_id},salt = 'gift-confirm')

    confirm_link = url_for('order_bp.confirm_gift',token = token , _external=True)
    cancel_link = url_for('order_bp.cancel_gift',token = token, _external = True)
    
    email_body = f"""
    Hello {customer.name},
    Greetings to you!!Please confirm your gift acceptance by clicking the link below:
    {confirm_link}
    If you do not want to accept this gift, please cancel by clicking here:
    {cancel_link}
    """
    
    verified_sender_email = "swaj718@gmail.com"
    message_id = make_msgid()
    message = Message("Confirm Gift Acceptance",sender=verified_sender_email,recipients=[customer.email],body=email_body,reply_to=customer.email)
    message.extra_headers={'Message-ID': message_id}
    mail.send(message)

    return message_id
    pass

def confirm_gift(token):
    serializer = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token, salt='gift-confirm', max_age=3600)  # expires in 1 hour - 3600
        order = Order.query.get(data['order_id'])
        if order:
            ####### customer email update #######

            customeraccnt = CustomerAccount.query.get(order.customeraccnt_id)
            customer = Customer.query.get(customeraccnt.customer_id)

            customer = Customer.query.get(customer_id)
            print("Customer name",customer.name)
            print("Customer email",customer.email)
            
            order.status = 'Confirmed'
            db.session.commit()
            #return {"Message": "Gift has been confirmed successfully"},201
            address_link = url_for('order_bp.submit_address',token = token , _external=True)

            email_body = f"""
            Hello {customer.name},
            Greetings to you!!Please provide your Shipping address for gift delivery by clicking the link below:
            {address_link}
            """
            sender_email = "swaj718@gmail.com"
            message = Message("Provide your Gift delivery address",sender=sender_email,recipients=[customer.email],body=email_body)

            original_message_id = data.get('msg_id')
            message.extra_headers ={
                'In-Reply-To': original_message_id,
                'References': original_message_id
            }
            mail.send(message)
            return {"Message": "Gift has been confirmed successfully, and Address email sent"}, 201
        else:
            return {"Message": "Order not found"},404
    except SignatureExpired:
        return {"message":"The confirmation link has expired"},400
    except BadSignature:
        return {"Message":"Invalid Token"},400

def cancel_gift(token):
    serializer = Serializer(current_app.config['SECRET_KEY'])
    try:
       data = serializer.loads(token, salt='gift-confirm',max_age=3600) 
       order = Order.query.get(data['order_id'])
       if order:
           order.status = 'Cancelled'
           db.session.commit()
           return {"Message":"Alas ,Order for the gift has been cancelled!!"},201
    except SignatureExpired:
        return {'Message':"The confirmation link has expired"},400
    except BadSignature:
        return {'Message':"Invalid Token"},400

def submit_address(token):
    html_content = render_template('form.html', token=token)
    # Create a response object with HTML content and correct MIME type
    response = make_response(html_content)
    response.headers['Content-Type'] = 'text/html'
    return response,201

def address_update(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            address = request.form.get('Address')
            print(address)
            data = serializer.loads(token, salt='gift-confirm',max_age=3600) 
            order = Order.query.get(data['order_id'])
            if order:
                order.status = 'Confirmed'
                order.delivery_address = address
                db.session.commit()
                db.session.refresh(order)
                return {"Message":"Address for order delivery successfully updated!"},201
            else:
                return {"Message": "Order not found"},404
        except SignatureExpired:
            return {'Message':"The confirmation link has expired"},400
        except BadSignature:
            return {'Message':"Invalid Token"},400

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
    query = select(Order).options(joinedload(Order.customer_account)).where(Order.id == id)
    order = db.session.execute(query).scalar_one_or_none()

    if order:
        db.session.delete(order)
        db.session.commit()
        return order,201
    else:
        return {"Message":"Order deletion failed"},404

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
