from flask import Flask
from database import db
from models.schemas import ma
from limiter import limiter
from caching import cache
from flask_swagger_ui import get_swaggerui_blueprint

from models.customer import Customer
from models.product import Product
from models.order import Order

from routes.customerBP import customer_blueprint
from routes.productBP import product_blueprint
from routes.orderBP import order_blueprint
from routes.customeraccntBP import customeraccnt_blueprint

#SWAGGER
SWAGGER_URL = '/api/docs' # URL endpoint for swagger api documentation
API_URL = '/static/swagger.yaml'

swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL,API_URL,config={'app_name':"Ecommerce API"})



def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    print('Running')
    return app

def blueprint_config(app):
    app.register_blueprint(customer_blueprint, url_prefix='/customers')
    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.register_blueprint(customeraccnt_blueprint, url_prefix='/customeraccnt')
    app.register_blueprint(swagger_blueprint,url_prefix=SWAGGER_URL)

def rate_limit_config():
    limiter.limit("20 per day")(customer_blueprint)
    limiter.limit("20 per day")(product_blueprint)
    limiter.limit("20 per day")(order_blueprint)


# @app.route('/sum', methods = ['POST'])
# def sum():
#     data = request.get_json()
#     num1 = data['num1']
#     num2 = data['num2']

#     result = num1 + num2 

#     return jsonify({"result":result})

app = create_app('DevelopmentConfig')

if __name__ == '__main__':

    blueprint_config(app)

    rate_limit_config()

    with app.app_context():
        #db.drop_all()
        db.create_all()

    app.run()