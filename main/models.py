### CourseWebApp.models
import os
import sqlite3

from flask import g
from werkzeug.exceptions import abort

from main import database


"""
	The Model class acts as proxy to the database as follows:
		- a Model corresponds to a database table row,
		- the Model's attributes to the row's entries and
		- Model methods to database operations.
	I.e.,
		Model instance	<~~~>	Table row
		Model.attribute	<~~~>	Row entry
		Model.method()	<~~~>	Database operation

	Data transfers between front-end and back precisely when
	Models interact with Forms.  (See 'main.forms' for the
	Form side of things.)  This ultimately comes down to
	interfacing the Model's __dict__ with the Form's
	formContent:

		Model.__dict__ 	<~~~>	Form.formContent

	That's the gist of it.

	N.B. All of the Model methods below amount to a database
	operation behind-the-scenes except for one key situation:
	when the method 'db_select' is set to 'all=True'.  In this
	case, the method returns data external to the Model class:
	an entire database table in the form of a list of dictionar-
	ies.  Cf. Methods 'db_insert', 'db_update', 'db_delete'.							
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
		return f"Model for database.  Use attribute '__dict__' for data."


	### Method for SQL SELECT operation
	def db_select(self, what:str='*', join=False, where:dict=None, order:str=None, limit:str=None, all=False):
		database.scrub(self.table)
		database.scrub_dict(locals())

		### Note: 'cursor' below is an sqlite3.Row.
		### See 'main.database.db_open' for the row factory configuration.
		cursor = database.db_query(
					self.table,
					what=what,
					join=join,
					where=where,
					order=order,
					limit=limit,
					all=all )

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


