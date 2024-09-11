from flask import jsonify,request
from models.schemas.productSchema import product_schema,products_schema 
from marshmallow import ValidationError
from services import productService
from caching import cache

def save():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages),400
    
    try:
        product_save = productService.save(product_data)
        return product_schema.jsonify(product_save),201
    except ValidationError as e:
        return jsonify({"error":str(e)}),400

@cache.cached(timeout=60)
def find_all():
    all_products = productService.find_all()
    return products_schema.jsonify(all_products),200    
    
def search_product():
    search_term = request.args.get("search")
    searched_item = productService.search_product(search_term)
    return products_schema.jsonify(searched_item)

def delete_product(id):
    response,status = productService.delete_product(id)
    if status!=201:
        return jsonify({f"message": "Sorry,Product with id specified is not available!!"}),status
    else:
        print("Product deleted successfully!!")
        return product_schema.jsonify(response),status
    
def update_product(id):
    try:
        data = request.json
        prod = productService.update_product(id,data)
        if not prod:
            return jsonify({"message": "Sorry,Product is not available!!"}),404
        else:
            return product_schema.jsonify(prod),201
        
    except ValidationError as e:
        return jsonify(e.messages),400
    
    