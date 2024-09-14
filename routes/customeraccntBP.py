from flask import Blueprint,jsonify,request
from controllers.customeraccountController import save,find_all,update_customeraccnt,delete_customeraccnt,create_custaccnt,login,get_account_by_id

customeraccnt_blueprint = Blueprint('customeraccnt_bp',__name__)

customeraccnt_blueprint.route('/',methods=['POST'])(save)
customeraccnt_blueprint.route('/', methods=['GET'])(find_all)

customeraccnt_blueprint.route('/<int:id>',methods=['DELETE'])(delete_customeraccnt)

customeraccnt_blueprint.route('/<int:id>',methods=['PUT'])(update_customeraccnt)
customeraccnt_blueprint.route('/login',methods=['POST'])(login)
#customeraccnt_blueprint.route('/', methods=['POST'])(create_custaccnt)

customeraccnt_blueprint.route('/<int:id>',methods = ['GET'])(get_account_by_id)
 