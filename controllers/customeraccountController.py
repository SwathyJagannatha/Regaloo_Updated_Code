from flask import request, jsonify
from models.schemas.customeraccountSchema import customeraccnt_schema, customeraccnts_schema
from services import customeraccountService #dont import the individual function, import the module as a whole
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required,admin_required

def save(): #name the controller will always be the same as the service function

    try:
        #try to validate the incoming data, and deserialize
        customeraccnt_data = customeraccnt_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer_saved = customeraccountService.save(customeraccnt_data)
    return customeraccnt_schema.jsonify(customeraccnt_data), 201

@cache.cached(timeout=60)
@admin_required
def find_all():
    all_customers = customeraccountService.find_all()
    return customeraccnts_schema.jsonify(all_customers),200

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
