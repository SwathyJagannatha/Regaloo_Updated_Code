
from flask import Blueprint,jsonify,request
from controllers.roleController import save,find_all,update_role,delete_role

role_blueprint = Blueprint('role_bp',__name__)

role_blueprint.route('/',methods=['POST'])(save)
role_blueprint.route('/', methods=['GET'])(find_all)

role_blueprint.route('/<int:id>',methods=['DELETE'])(delete_role)

role_blueprint.route('/<int:id>',methods=['PUT'])(update_role)
