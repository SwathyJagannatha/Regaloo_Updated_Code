from . import ma
from marshmallow import fields

class CustomerAccountSchema(ma.Schema):
    id = fields.Integer(required=False)
    username = fields.String(required=True)
    password = fields.String(required=True)
    customer_id = fields.Integer(required=True)
    customer = fields.Nested('CustomerOrderSchema')

    class Meta:
        fields = ("id","username","password","customer_id","customer")

customeraccnt_schema = CustomerAccountSchema()
customeraccnts_schema = CustomerAccountSchema(many=True)

