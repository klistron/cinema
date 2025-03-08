import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://test:test@localhost/test'
SECRET_KEY = "whhfsdfpsflweazczlczlcvxcv"

SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False