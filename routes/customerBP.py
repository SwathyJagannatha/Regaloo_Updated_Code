from flask import Blueprint,jsonify,request
from controllers.customerController import save,find_all,delete_customer,update_customer

customer_blueprint = Blueprint('customer_bp',__name__)

customer_blueprint.route('/',methods=['POST'])(save)
customer_blueprint.route('/', methods=['GET'])(find_all)

customer_blueprint.route('/<int:id>',methods=['DELETE'])(delete_customer)

customer_blueprint.route('/<int:id>',methods=['PUT'])(update_customer)

#get_customer_by_id
#customer_blueprint.route('/search/<int:id>',methods=['GET'])(get_customer_by_id)
