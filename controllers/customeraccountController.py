from flask import request, jsonify
from models.schemas.customeraccountSchema import customeraccnt_schema, customeraccnts_schema
from services import customeraccountService #dont import the individual function, import the module as a whole
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required,admin_required


def login():
    try:
        credentials = request.json
        token, success = customeraccountService.login(credentials['username'], credentials['password'])
        if success:
            return jsonify({"auth_token": token, "status": "success"}), 200
        else:
            return jsonify({"message": "Invalid username or password", "status": "fail"}), 401  # Now returns 401 if login fails
    except KeyError:
        return jsonify({'message': 'Invalid payload, expecting username and password', "status": "fail"}), 400 

def get_account_by_id(id):
    try:
        customer_accnt = customeraccountService.get_account_by_id(id)

        if not customer_accnt:
           return jsonify({"message": "Sorry,CustomerAccnt not found!!"}),404 
        else:
           return customeraccnt_schema.jsonify(customer_accnt),201 
    except ValidationError as e:
        return jsonify(e.messages), 400

def update_customeraccnt(id): #name the controller will always be the same as the service function
    try:
        data = request.json
        #try to validate the incoming data, and deserialize
        customeraccnt=customeraccountService.update_customeraccnt(id,data)

        if not customeraccnt:
            return jsonify({"message": "Sorry,CustomerAccnt not found!!"}),404
        else:
            return customeraccnt_schema.jsonify(customeraccnt), 201
        
    except ValidationError as e:
        return jsonify(e.messages), 400
    
def save(): #name the controller will always be the same as the service function

    try:
        #try to validate the incoming data, and deserialize
        customeraccnt_data = customeraccnt_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    response,status = customeraccountService.save(customeraccnt_data)

    if status != 201:
        return jsonify(response),status
    return customeraccnt_schema.jsonify(customeraccnt_data), status

def create_custaccnt():
    try:
        account_data = customeraccnt_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    response,status = customeraccountService.create_custaccnt(account_data)

    if status != 201:
        return jsonify(response),status
    return customeraccnt_schema.jsonify(account_data), status


@cache.cached(timeout=60)
# @token_required
def find_all():
    response,status = customeraccountService.find_all()
    if status != 201:
        return jsonify(response),status
    return customeraccnts_schema.jsonify(response), status

# def find_all_paginate():
#     page = int(request.args.get('page'))
#     per_page = int(request.args.get('per_page'))
#     customeraccnts = customerService.find_all_paginate(page, per_page)
#     return customeraccnts_schema.jsonify(customeraccnts), 200

# def delete_customer(id):
#     customer=customerService.delete_customer(id)
#     if customer:
#        return customer_schema.jsonify(customer),200
#     else:
#         return jsonify({"message": "Sorry,Customer not found!!"}),404
    
def update_customeraccnt(id): #name the controller will always be the same as the service function
    try:
        data = request.json
        #try to validate the incoming data, and deserialize
        customeraccnt=customeraccountService.update_customeraccnt(id,data)

        if not customeraccnt:
            return jsonify({"message": "Sorry,CustomerAccnt not found!!"}),404
        else:
            return customeraccnt_schema.jsonify(customeraccnt), 201
        
    except ValidationError as e:
        return jsonify(e.messages), 400
    
def delete_customeraccnt(id):
    customeraccnt=customeraccountService.delete_customeraccnt(id)
    if customeraccnt:
       return customeraccnt_schema.jsonify(customeraccnt),200
    else:
        return jsonify({"message": "Sorry,Customer Account not found!!"}),404
