import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET KEY') or 'secret'
	DATABASE = 'db.sqlite'
	CKEDITOR_PKG_TYPE = 'full'
