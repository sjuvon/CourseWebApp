import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET KEY') or 'secret'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
	CKEDITOR_PKG_TYPE = 'full'
