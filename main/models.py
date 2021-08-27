### CourseWebApp.models
import os
import sqlite3

from flask import g
from werkzeug.exceptions import abort

from main import database
from main import functions


"""
	Some words on the following construction (and the app
	philosophy in general):

	The main idea is to use the Model class below as proxy
	to the database; this is done in the following way:
		- a Model instance corresponds to a database table,
		- the Model's attributes to the corresponding
		  table's columns, and
		- Model methods to database operations.
	E.g.,
		Model instance		<~~~>	Database table
		Model.attribute		<~~~>	Table column
		Model.method		<~~~>	Table operation

	With this in hand, we transfer user-data to and from
	the database by having Model classes interact with Form
	classes.  (See 'main.forms' for the Form side of things.)
	This is ultimately done by having the Model's model.__dict__
	interact with the Form's form.formContent.

	That's the gist of the app.  Sadly, there is one important
	place where the

		Model <~~~> Database

	correspondence unfortunately breaks down: when the Model
	method 'db_select' is set to 'all=True'.  In this case,
	the method does not render the Model's attributes as
	database entries; instead, it returns a list of database
	rows (with each row as a dictionary).  This makes things
	much easier to work with Views.
																"""


### BEGIN CLASS Model
class Model():

	__slots__ = ('table', 'length', 'author_id', '__dict__')

	### Initialise Model instance with database
	### entries for attributes.
	def __init__(self, **kwargs):
		for key, value in kwargs.items():
			setattr( self, f"{key}", f"{value}" )

	def __repr__(self):
		return f"Model for database operations.  Use attribute '__dict__' for database table's columns."


	### Method for SQL SELECT operation
	def db_select(self, what:str='*', join=False, where:dict=None, order:str=None, limit:str=None, all=False):
		database.scrub(self.table)
		database.scrub_dict(locals())

		### Note: 'cursor' below is an sqlite3.Row.
		### See 'main.database' for the row factory configuration.
		cursor = database.db_query(self.table, what=what, join=join, where=where, order=order, limit=limit, all=all)

		if cursor is None:
			abort(404, f"{getattr(self.table,'capitalize')()} {id} doesn't exist.")
		else:
			content = [ dict(row) for row in cursor ] if all else dict(cursor)

			if all:
				return content
			else:
				self.__dict__ = dict(cursor)
																	### END METHOD db_select


	### Method for SQL INSERT operation
	def db_insert(self):
		database.scrub(self.table)
		database.scrub_list(self.__dict__.keys())

		db = database.db_open()

		query = database.db_queryBuilder(
					operation='INSERT',
					table=self.table,
					dictionary=self.__dict__ )

		db.execute(query, self.__dict__)
		db.commit()
																	### END METHOD db_insert


	### Method for SQL UPDATE operation
	def db_update(self, idd:int):
		database.scrub(self.table)
		database.scrub(str(idd))
		database.scrub_list(self.__dict__.keys())

		db = database.db_open()

		query = database.db_queryBuilder(
			operation='UPDATE',
			table=self.table,
			idd=idd,
			dictionary=self.__dict__ )

		db.execute(query, self.__dict__)
		db.commit()
																	### END METHOD db_update


	### Method for SQL DELETE operation
	def db_delete(self, id:int):
		database.scrub(self.table)
		database.scrub(str(id))

		db = database.db_open()

		db.execute(f"DELETE FROM {self.table} WHERE id = ?", (id,))
		db.commit()
																	### END METHOD db_delete

																	### END CLASS Model


