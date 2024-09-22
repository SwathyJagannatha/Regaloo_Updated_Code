from marshmallow import fields,validate
from . import ma

class OrderSchema(ma.Schema):
    id = fields.Integer(required = False)
    date = fields.Date(required = False)
    customeraccnt_id = fields.Integer(required=True)
    products = fields.Nested('ProductSchema',many=True)
    product_ids = fields.List(fields.Integer())
    customer = fields.Nested('CustomerSchema')
    status = fields.String(missing = 'pending')
    total_amt = fields.Decimal(as_string=True)
    delivery_address = fields.String(required=False)

    recipient_email = fields.Email(required=True)
    recipient_name = fields.String(required =True)
    sender_name = fields.String(required =True)
    gift_message = fields.String(required =True)

    class Meta:
        fields = ('id','date','customeraccnt_id','products','status','total_amt','delivery_address','recipient_email','recipient_name','sender_name','gift_message')

order_schema = OrderSchema()
orders_schema = OrderSchema(many = True)
