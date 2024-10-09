from flask import Blueprint
from controllers.orderController import find_all,save,send_shipping_email,find_by_id,find_by_customer_id,find_by_customer_email,send_confirm_email,confirm_gift,cancel_gift,address_update,submit_address,delete_order,update_order,create_order,cancel_gift_redirect

order_blueprint = Blueprint('order_bp',__name__)
#order_blueprint.route('/',methods=['POST'])(save)

order_blueprint.route('/',methods=['POST'])(create_order)
order_blueprint.route('/',methods=['GET'])(find_all)
order_blueprint.route('/<int:id>',methods=['DELETE'])(delete_order)

order_blueprint.route('/<int:id>',methods=['GET'])(find_by_id)

order_blueprint.route('/<int:id>/<int:order_id>',methods=['POST'])(send_confirm_email)

order_blueprint.route('/address_update/<token>',methods=['POST'])(address_update)
order_blueprint.route('/submit_address/<token>',methods=['GET'])(submit_address)

order_blueprint.route('/customer/<int:id>',methods=['GET'])(find_by_customer_id)
order_blueprint.route('/customer/email',methods=['POST'])(find_by_customer_email)

order_blueprint.route('/<int:id>',methods=['PUT'])(update_order)

order_blueprint.route('/confirm_gift/<token>',methods=['GET'])(confirm_gift)
order_blueprint.route('/cancel_gift/<token>',methods=['GET'])(cancel_gift)

order_blueprint.route('/cancel_gift_redirect/<token>',methods=['GET'])(cancel_gift_redirect)
order_blueprint.route('/shipping',methods=['POST'])(send_shipping_email)


