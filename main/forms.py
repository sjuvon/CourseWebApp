### CourseWebApp.Forms

"""
	Module for webform used throughout app
	E.g.,	See modules:
			'announcements'
			'homework'
			'lectures'
			'welcome'	(Located in main view)
	N.B.	The Authentication module 'auth'
			uses its own special form.
											"""

from flask import flash
from flask import g
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import IntegerField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import ValidationError

from main import database
from main import functions
from main import models


"""
	Comment on the constructions below
											"""


### BEGIN CLASS Form (Generic base form)
class Form(FlaskForm):
	submit = SubmitField()
	formContent = {}

	### To update form after user input
	### for eventual database entry
	def formulateContent(self):
		Fields = { 'CSRFTokenField', 'SubmitField' }
		for field in self:
			if field.type not in Fields:
				if field.type == 'FileField':
					filename = functions.upload(field.data, self.table)
					self.formContent[field.name] = filename
				else:
					self.formContent[field.name] = field.data

	### For displaying validation errors
	### from user input
	def outtakes(self):
		if self.errors:
			for error in self.errors.values():
				flash(*error)
																			### END CLASS Form


### BEGIN CLASS Form_Create
def Formula_Create(*args, **kwargs):
	class Form_Create(Form):

		### The only custom validator
		def validate_Zahl(self,Zahl):
			if self.table == 'homework' or self.table =='lecture':
				check_exists = database.db_query(
										self.table,
										what='Zahl',
										where={ 'id': self.Zahl.data },
										all=False)
		
				### To verify that we're creating a valid lecture/assignment
				if check_exists:
					Table = self.table.capitalize()
					raise ValidationError(f"{Table} {self.Zahl.data} already exists")


	Fach = { 'File', 'Integer', 'String', 'TextArea', 'CKEditor' }
	for key, value in kwargs.items():
		if value not in Fach:
			setattr( Form_Create, f'{key}', f'{value}' )

			if key != 'table':
				Form_Create.formContent[key] = value

		else:	
			label = f"{key}".capitalize()
			field = eval(f"{value}Field")(label)
			setattr( Form_Create, f"{key}", field )

			Form_Create.formContent[key] = None


	return Form_Create()
																			### END CLASS Form_Create


### BEGIN CLASS Form_Update
def Formula_Update(**kwargs):
	class Form_Update(Form):

		### The only custom validator
		def validate_Zahl(self,Zahl):
			if self.table == 'homework' or self.table =='lecture':
				check_exists = database.db_query(
									self.table,
									what='Zahl',
									where={'id':self.Zahl.data},
									all=False)
		
				### To verify that we're updating the correct lecture/assignment
				if self.Zahl.data != self.formContent['id']:
					Table = self.table.capitalize()
					raise ValidationError(f"{Table} {self.Zahl.data} already exists.  This is {Table} {self.formContent['id']}.") \
						if check_exists else ValidationError(f"{Table} {self.Zahl.data} does not exist.  This is {Table} {self.formContent['id']}.")


	Fach = { 'File', 'Integer', 'String', 'TextArea', 'CKEditor' }
	for key, value in kwargs.items():
		if type(value) != tuple:
			setattr( Form_Update, f'{key}', f'{value}')
			if key != 'table':
				Form_Update.formContent[key] = value

		else:
			label = f"{key}".capitalize()
			field = eval(f"{value[0]}Field")(label)
			setattr( Form_Update, f"{key}", field )

			Form_Update.formContent[key] = value[1]


	return Form_Update(**Form_Update.formContent)
																			### END CLASS Form_Update

