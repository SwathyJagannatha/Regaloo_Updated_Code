from flask import request, jsonify
from models.schemas.customerSchema import customer_schema, customers_schema
from services import customerService #dont import the individual function, import the module as a whole
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required,admin_required

def save(): #name the controller will always be the same as the service function

    try:
        #try to validate the incoming data, and deserialize
        customer_data = customer_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer_saved = customerService.save(customer_data)
    return customer_schema.jsonify(customer_saved), 201

#@admin_required
@cache.cached(timeout=60)
def find_all():
    all_customers = customerService.find_all()
    return customers_schema.jsonify(all_customers),200

def find_all_paginate():
    page = int(request.args.get('page'))
    per_page = int(request.args.get('per_page'))
    customers = customerService.find_all_paginate(page, per_page)
    return customers_schema.jsonify(customers), 200

def delete_customer(id):
    customer=customerService.delete_customer(id)
    if customer:
       return customer_schema.jsonify(customer),200
    else:
        return jsonify({"message": "Sorry,Customer not found!!"}),404
    
def update_customer(id): #name the controller will always be the same as the service function
    try:
        data = request.json
        #try to validate the incoming data, and deserialize
        customer=customerService.update_customer(id,data)

        if not customer:
            return jsonify({"message": "Sorry,Customer not found!!"}),404
        else:
            return customer_schema.jsonify(customer), 201
        
    except ValidationError as e:
        return jsonify(e.messages), 400
