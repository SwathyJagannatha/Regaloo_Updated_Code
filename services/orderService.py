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
from flask import redirect

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
    gift_mess = data.get('gift_message')
    recip_email = data.get('recipient_email')
    recip_name = data.get('recipient_name')
    sender_name = data.get('sender_name')

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

    # for order in orders_obj:
    #     existing_prods = [
    #         { "id" : prod.id , "quantity": prod.stock_qty, "description": prod.description}
    #         for prod in order.products
    #     ]

    #     if compare_products(existing_prods,product_ids):
    #         return {"Message": "Duplicate order found for same customer id with same product list"},404

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
    latest_order = Order(date=datetime.now(), customeraccnt_id=custaccount_id, gift_message = gift_mess, recipient_email = recip_email, recipient_name = recip_name, sender_name = sender_name,total_amount=total_amt, status="Pending Order")

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
            "gift_message": latest_order.gift_message,
            "recipient_name": latest_order.recipient_name,
            "recipient_email": latest_order.recipient_email,
            "sender_name": latest_order.sender_name,
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
    token = s.dumps({'custaccnt_id': custaccnt_id,'order_id':order_id},salt = 'gift-confirm')

    order = Order.query.get(order_id)

    confirm_link = url_for('order_bp.confirm_gift',token = token , _external=True)
    cancel_link = url_for('order_bp.cancel_gift',token = token, _external = True)
    
    # HTML Email Body with buttons
    email_body = f"""
    <html>
      <body>
	   <div style="width: 600px; height: 554px; background-color: white; padding: 20px; font-family: Arial, sans-serif;">
        <!-- Logo or Image -->
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://via.placeholder.com/126x55" alt="Logo" style="width: 126px; height: 55px;" />
        </div>

        <!-- Greeting and Message -->
        <div style="padding-bottom: 10px;">
            <p style="font-size: 16px; font-weight: bold; margin: 0;">Dear {order.recipient_name},</p>
            <p style="font-size: 14px; margin: 0;">This is a gift from {order.sender_name}, with message : {order.gift_message}.</p>
        </div>

        <!-- Accept Button Section -->
        <div style="padding-top: 20px;">
	        <p style="font-size: 14px;">I’m pleased to inform you that a special surprise is on its way to you.</p>
            <p style="font-size: 14px;">Please confirm your gift acceptance by clicking the button below:</p>
            <div style="text-align: center; margin-top: 10px;">
                <a href="{confirm_link}" style="display: inline-block; background-color: #4ca330; color: #f1faeb; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 14px; font-weight: bold;">Accept Gift & Continue</a>
            </div>
        </div>

        <!-- Decline Button Section -->
        <div style="padding-top: 20px;">
            <p style="font-size: 14px;">If you do not want to accept this gift, please cancel by clicking the button below:</p>
            <div style="text-align: center; margin-top: 10px;">
                <a href="{cancel_link}" style="display: inline-block; color: #4ca330; padding: 10px 20px; text-decoration: none; border: 2px solid #4ca330; border-radius: 5px; font-size: 14px; font-weight: bold;">Decline Gift</a>
            </div>
        </div>

        <!-- Closing -->
        <div style="padding-top: 40px;">
            <p style="font-size: 14px;">Best Regards,</p>
            <p style="font-size: 14px;">Regalooo Team</p>
        </div>
      </div>
      </body>
   
    </html>
    """

    # HTML Email body for sender
    email_body_sender = f"""
    <html>
    <body>
    <div style="width: 600px; height: 554px; background-color: white; padding: 20px; font-family: Arial, sans-serif;">
        <div style="padding-bottom: 10px;">
            <p style="font-size: 16px; font-weight: bold; margin: 0;">Dear {order.sender_name},</p>
            <p style="font-size: 14px; margin: 0;">We’ve sent an email to your recipient, letting them know about their special gift. 
            They’ll be prompted to securely provide their delivery address, once they accept the gift.</p>
        </div>

        <div style="padding-top: 20px;">
	        <p style="font-size: 14px;">Once they’ve confirmed their details, we'll notify you and guide you through the final steps to ship the gift.
            Keep an eye on your inbox for updates – we’ll notify you as soon as the recipient approves and provides their address!</p>
        </div>

        <!-- Closing -->
        <div style="padding-top: 40px;">
            <p style="font-size: 14px;">Best Regards,</p>
            <p style="font-size: 14px;">Regalooo Team</p>
        </div>
    </div>
    </body>
    </html>
    """
    
    subject = f"{order.sender_name} has sent you a gift!!"
    verified_sender_email = "noreply@regalooo.com"

    message = Message(subject,sender=verified_sender_email,recipients=[order.recipient_email],html=email_body,reply_to=customer.email)
    mail.send(message)

    message = Message("Your gift is almost Ready!",sender=verified_sender_email,recipients=[customer.email],html=email_body_sender,reply_to=customer.email)
    mail.send(message)

def confirm_gift(token):
    serializer = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token, salt='gift-confirm', max_age=3600)  # expires in 1 hour - 3600
        order = Order.query.get(data['order_id'])
        if order:
            customeraccnt = CustomerAccount.query.get(order.customeraccnt_id)
            customer = Customer.query.get(customeraccnt.customer_id)

            print("Customer name",customer.name)
            print("Customer email",customer.email)
            
            order.status = 'Confirmed'
            db.session.commit()

            sender_email_body = f"""
            Your Gift is on its Way!

            Great news! The recipient has approved their address, and you've successfully set the shipping method. Your order is now on its way!
            Tracking Information:
            Carrier: UPS
            Tracking Number: 1Z12345E6205277936
            Estimated Delivery: 10, 2024
            We've sent all the details, including tracking information, to your email. Be sure to check it for updates. Your recipient has also received an email with tracking information, so they can follow the progress of their gift as well.

            Thank you for choosing Regaloo to send your special gift!

            Warm Regards,
            Regaloo Team
            """

            # sender_email = "noreply@regalooo.com"
            # message = Message("Your Gift is on its Way",sender=sender_email,recipients=[customer.email],body=sender_email_body)
            # mail.send(message)

            return submit_address(token)
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
           return cancel_gift_redirect(token)
    except SignatureExpired:
        return {'Message':"The confirmation link has expired"},400
    except BadSignature:
        return {'Message':"Invalid Token"},400

def submit_address(token):
    # Construct the URL of the Vercel app with the token as a query parameter
    vercel_url = f"https://regaloowebsite.vercel.app/shipping?token={token}"
    
    # Redirect the user to the Vercel app's shipping form pageupdated
    return redirect(vercel_url, code=302)

def cancel_gift_redirect(token):
    # Construct the URL of the Vercel app with the token as a query parameter
    vercel_url = f"https://regaloowebsite.vercel.app?token={token}"
    
    # Redirect the user to the Vercel app's shipping form pageupdated
    return redirect(vercel_url, code=302)

def address_update(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            address = request.json.get('address1')
            address2 = request.json.get('address2')
            city = request.json.get('city')
            state = request.json.get('state')
            zip_code = request.json.get('zipCode')
            email = request.json.get('email')
            
            data = serializer.loads(token, salt='gift-confirm',max_age=3600) 
            order = Order.query.get(data['order_id'])
            if order:

                customeraccnt = CustomerAccount.query.get(order.customeraccnt_id)
                customer = Customer.query.get(customeraccnt.customer_id)

                order.status = 'Confirmed'
                order.delivery_address = f" {address}, {address2}, {city}, {state}, {zip_code}"
                db.session.commit()
                db.session.refresh(order)
                # return {"Message":"Address for order delivery successfully updated!"},201

                # email to recipient saying address succesfully submitted 
                # HTML Email Body with buttons
                email_body = f"""
                <html>
                  <body>
	                <div style="width: 600px; height: 554px; background-color: white; padding: 20px; font-family: Arial, sans-serif;">
        
                    <!-- Greeting and Message -->
                    <div style="padding-bottom: 10px;">
                        <p style="font-size: 16px; font-weight: bold; margin: 0;">Dear {order.recipient_name},</p>
                        <p style="font-size: 14px; margin: 0;">Your Gift is almost Ready!</p>
                    </div>

                    <div style="padding-top: 20px;">
	                    <p style="font-size: 14px;">Thanks for providing your delivery details!
                        The sender will now complete the final steps to ship your gift.
                        Stay tuned – we’ll send you an email with tracking information as soon as the gift is on its way. 
                        Keep an eye on your inbox for updates!</p>
                    </div>

                    <div style="padding-top: 20px;">
                        <div style="text-align: center; margin-top: 10px;">
                        <a href="https://regaloowebsite.vercel.app/" style="display: inline-block; color: #4ca330; padding: 10px 20px; text-decoration: none; border: 2px solid #4ca330; border-radius: 5px; font-size: 14px; font-weight: bold;">Go Home</a>
                    </div>

                    <!-- Closing -->
                    <div style="padding-top: 40px;">
                        <p style="font-size: 14px;">Best Regards,</p>
                        <p style="font-size: 14px;">Regalooo Team</p>
                    </div>
                    </div>
                  </body>
                </html>
                """

              # HTML Email body for sender
                email_body_sender = f"""
                <html>
                <body>
                    <div style="width: 600px; height: 554px; background-color: white; padding: 20px; font-family: Arial, sans-serif;">
                        <div style="padding-bottom: 10px;">
                            <p style="font-size: 16px; font-weight: bold; margin: 0;">Dear {order.sender_name},</p>
                            <p style="font-size: 14px; margin: 0;">Your recipient provided their address successfully.
                        </div>

                        <div style="padding-top: 20px;">
	                        <p style="font-size: 14px;">You can submit the order for shipping through this link: </p>
                            <a href="https://regaloowebsite.vercel.app/orders" style="display: inline-block; color: #4ca330; padding: 10px 20px; text-decoration: none; border: 2px solid #4ca330; border-radius: 5px; font-size: 14px; font-weight: bold;">Place Order</a>
                        </div>

                        <!-- Closing -->
                        <div style="padding-top: 40px;">
                            <p style="font-size: 14px;">Best Regards,</p>
                            <p style="font-size: 14px;">Regalooo Team</p>
                        </div>
                    </div>
                </body>
                </html>
                """

                subject = f"{order.sender_name} has sent you a gift!!"
                verified_sender_email = "noreply@regalooo.com"

                message = Message(subject,sender=verified_sender_email,recipients=[order.recipient_email],html=email_body)
                mail.send(message)

                message = Message("Your gift is almost Ready!",sender=verified_sender_email,recipients=[customer.email],html=email_body_sender,reply_to=customer.email)
                mail.send(message)

                # email to sender 
                return {"Message": "Address for order delivery successfully updated!"}, 201
            else:
                return {"Message": "Order not found"},404
        except SignatureExpired:
            return {'Message':"The confirmation link has expired"},400
        except BadSignature:
            return {'Message':"Invalid Token"},400

# def complete_shipping(order_id):
#     order = Order.query.get(order_id)
#     if order:
#         order.status = 'Shipped'
#     pass

def send_shipping_email():

    data = request.get_json()
    order_id = data.get('order_id')

    if not order_id:
        return {"Message": "Order ID is required"}, 400
    
    order = Order.query.get(order_id)
    if order:
        if order.status == "Shipped":
           # Email body for the recipient with tracking details
            recipient_email_body = f"""
            <html>
            <body>
            <p>Dear {order.recipient_name},</p>
            <p>Your order has been shipped! You can track your gift with the details below:</p>
            <ul>
                <li>Carrier: UPS</li>
                <li>Tracking Number: 1Z12345E6205277936</li>
                <li>Estimated Delivery: '10/22/2024'</li>
            </ul>
            <p>Thank you for choosing Regaloo!</p>
            <p>Best regards,</p>
            <p>Regaloo Team</p>
            </body>
            </html>
            """

             # Send the email to the recipient
            verified_sender_email = "noreply@regalooo.com"
            message = Message("Your Gift is on its Way!", sender=verified_sender_email, recipients=[order.recipient_email], html=recipient_email_body)
            mail.send(message)

            return {"Message": "Shipping email sent successfully!"}, 200

        else:
            return {"Message": "Order is not marked as shipped!"}, 400
    else:
        return {"Message": "Order not found!"}, 404 

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
