from . import ma
from marshmallow import fields

class CustomerAccountSchema(ma.Schema):
    id = fields.Integer(required=False)
    username = fields.String(required=True)
    password = fields.String(required=True)
    customer_id = fields.Integer(required=True)
    role_id = fields.Integer(required=True)

    customer = fields.Nested('CustomerSchema',dump_only=True)

    class Meta:
        fields = ("id","username","password","customer_id","customer","role_id")

customeraccnt_schema = CustomerAccountSchema()
customeraccnts_schema = CustomerAccountSchema(many=True)

