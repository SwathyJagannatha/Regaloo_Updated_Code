import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Swa123sweet%40@localhost/advanced_e_comm'
    CACHE_TYPE = 'SimpleCache'
    DEBUG = True

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///app.db'
    CACHE_TYPE = 'SimpleCache'
    DEBUG = True

# Configuring mail settings
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('SENDGRID_USERNAME', 'apikey')  # Defaults to 'apikey' if not set
    MAIL_PASSWORD = os.environ.get('SENDGRID_PASSWORD')  # No default to ensure security
