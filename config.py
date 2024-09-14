import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Swa123sweet%40@localhost/advanced_e_comm'
    CACHE_TYPE = 'SimpleCache'
    DEBUG = True

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///app.db'
    CACHE_TYPE = 'SimpleCache'
    DEBUG = True

     # Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587 #465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'swaj718@gmail.com'
    MAIL_PASSWORD = 'aunf gvkq wsfe pndd'