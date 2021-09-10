### CourseWebApp.setup
from setuptools import find_packages
from setuptools import setup

setup(
	name='CourseWebApp',
	version='1.0',
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		'Flask>=2.0.1',
		'Flask-WTF>=0.15.1',
		'Flask-CKEditor>=0.4.6',
		'SQLAlchemy>=1.4.23'
		]
	)
