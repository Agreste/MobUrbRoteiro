import os

# Get application base dir.
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
RELOAD = True
SECRET_KEY = 'mysecretkeyvalue'
# SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(_basedir, 'db/app_dev.db')

SQLALCHEMY_DATABASE_URI = 'postgresql://moburb:moburb@localhost/moburb'
