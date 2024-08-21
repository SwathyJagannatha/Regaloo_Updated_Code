from flask import Blueprint
from controllers.orderController import find_all,save,find_by_id,find_by_customer_id,find_by_customer_email,delete_order,update_order

order_blueprint = Blueprint('order_bp',__name__)
order_blueprint.route('/',methods=['POST'])(save)
order_blueprint.route('/',methods=['GET'])(find_all)
order_blueprint.route('/<int:id>',methods=['DELETE'])(delete_order)

order_blueprint.route('/<int:id>',methods=['GET'])(find_by_id)
order_blueprint.route('/customer/<int:id>',methods=['GET'])(find_by_customer_id)
order_blueprint.route('/customer/email',methods=['POST'])(find_by_customer_email)

order_blueprint.route('/<int:id>',methods=['PUT'])(update_order)