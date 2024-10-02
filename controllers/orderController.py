from flask import jsonify,request
from models.schemas.orderSchema import order_schema,orders_schema 
from marshmallow import ValidationError
from services import orderService
from utils.util import user_token_wrapper
from caching import cache

def save():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages),400

    new_order = orderService.save(order_data)
    return order_schema.jsonify(new_order),201

def create_order():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages),400

    response,status = orderService.create_order(order_data)

    if status != 201:
        return jsonify(response),status 
    return order_schema.jsonify(response), status

def send_confirm_email(custaccnt_id,order_id):
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages),400

    response,status = orderService.send_confirm_email(custaccnt_id,order_id)

    if status != 201:
        return jsonify(response),status 
    return order_schema.jsonify(response), status


def confirm_gift(token):
    response = orderService.confirm_gift(token)
    return response

def cancel_gift(token):
    response = orderService.cancel_gift(token)
    return jsonify(response)

def address_update(token):
    response,status = orderService.address_update(token)
    return jsonify(response)

def submit_address(token):
    response,status = orderService.submit_address(token)
    return response

def cancel_gift_redirect():
    response = orderService.cancel_gift_redirect()
    return jsonify(response)

@cache.cached(timeout=60)
def find_all():
    all_orders = orderService.find_all()
    return orders_schema.jsonify(all_orders),200    
    
def find_by_id(id):
    orders = orderService.find_by_id(id)
    if not orders:
        return {"Message" : "Order with specified id doesnt exist"},404
    return orders_schema.jsonify(orders),200

@user_token_wrapper
def find_by_customer_id(id,token_id):
    if id == token_id:
        orders = orderService.find_by_customer_id(id)
    else:
        return jsonify({"message": "You cant view other peoples orders"})
    return orders_schema.jsonify(orders),200

@cache.cached(timeout=60)
def find_by_customer_email():
    email = request.json['email']
    orders = orderService.find_by_customer_email(email)
    return orders_schema.jsonify(orders),200

def delete_order(id):
    response,status = orderService.delete_order(id)
    if status!=201:
        #return jsonify({"message": "Sorry,Order ot found!!"}),404
        return jsonify(response),status
    else:
        print("Order deleted successfully!!")
        return order_schema.jsonify(response),status
    
def update_order(id):
    try:
        data = request.json 
        order = orderService.update_order(id,data)
        if not order:
            return jsonify({"message": "Sorry,Order is not available!!"}),404
        else:
            return order_schema.jsonify(order),201
    except ValidationError as e:
        return jsonify(e.messages),400