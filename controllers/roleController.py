from flask import request, jsonify
from models.schemas.roleSchema import role_schema, roles_schema
from services import roleService #dont import the individual function, import the module as a whole
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required,admin_required

def save(): #name the controller will always be the same as the service function
    try:
        #try to validate the incoming data, and deserialize
        role_data = role_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    role_saved = roleService.save(role_data)
    return role_schema.jsonify(role_saved), 201

@cache.cached(timeout=60)
def find_all():
    all_roles = roleService.find_all()
    return roles_schema.jsonify(all_roles),200

def delete_role(id):
    role=roleService.delete_role(id)
    if role:
       return role_schema.jsonify(role),200
    else:
        return jsonify({"message": "Sorry,Role not found!!"}),404
    
def update_role(id): #name the controller will always be the same as the service function
    try:
        data = request.json
        #try to validate the incoming data, and deserialize
        role=roleService.update_role(id,data)

        if not role:
            return jsonify({"message": "Sorry,role not found!!"}),404
        else:
            return role_schema.jsonify(role), 201
        
    except ValidationError as e:
        return jsonify(e.messages), 400