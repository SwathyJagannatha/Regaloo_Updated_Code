from marshmallow import fields,validate
from . import ma

class RoleSchema(ma.Schema):
    id = fields.Integer(required = False)
    role_name = fields.String(required = True)
    
    class Meta:
        fields = ("id","role_name")

role_schema = RoleSchema()
roles_schema = RoleSchema(many = True)


