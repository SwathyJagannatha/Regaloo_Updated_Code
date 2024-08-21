from flask import Blueprint
from controllers.productController import find_all,save,search_product,delete_product,update_product

product_blueprint = Blueprint('product_bp',__name__)
product_blueprint.route('/',methods=['POST'])(save)
product_blueprint.route('/<int:id>',methods=['DELETE'])(delete_product)

product_blueprint.route('/',methods=['GET'])(find_all)
product_blueprint.route('/search',methods=['GET'])(search_product)

product_blueprint.route('/<int:id>',methods=['PUT'])(update_product)