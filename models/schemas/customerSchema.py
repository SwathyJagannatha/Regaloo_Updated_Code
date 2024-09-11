from . import ma
from marshmallow import fields

class CustomerSchema(ma.Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ("id","name","email","phone")

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

class CustomerOrderSchema(ma.Schema):
    name = fields.String(required = True)
    email = fields.Email(required = True)
