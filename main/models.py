### CourseWebApp.models
import os
import sqlite3

from flask import g
from werkzeug.exceptions import abort

from main import database
from main import functions


"""
	Some words on the following construction:
	The main idea is to use each Model instance as a proxy
	for a database table.  The Model's attributes
	would correspond 1:1 to the table's columns: e.g.,

		Model.attribute		<~~~>	 Table column 'attribute'

	This means a row of the table would correspond to a
	'section' of the model: a choice of element from each
	attribute.  Note that this means the row order is implicitly
	the left-right order when reading attribute entries (so each
	Model attribute is a Python list).  In particular, the
	attributes of a given Model must all have the same number
	of elements.

		That said, there will be some special attributes for a
	Model: e.g., 'table', 'length'.  Here, the former is a string
	that records which database table the Model corresponds to,
	while 'length' is an integer corresponding to the table's
	number of rows.
																"""


### BEGIN CLASS Model
class Model():

	__slots__ = ('table', 'length', 'author_id', '__dict__')

	def __init__(self, **kwargs):
		for key, value in kwargs.items():
			setattr( self, f"{key}", f"{value}" )

	def __repr__(self):
		return f"Model for database operations.  Use attribute '__dict__' for database table's columns."


	### SELECT entry from database
	def db_select(self, what:str='*', join=False, where:dict=None, order:str=None, limit:str=None, all=False):
		database.scrub(self.table)
		database.scrub_dict(locals())

		cursor = database.db_query(self.table, what=what, join=join, where=where, order=order, limit=limit, all=all)
		if cursor is None:
			abort(404, f"{getattr(self.table,'capitalize')()} {id} doesn't exist.")
		else:
			### The following is possible since 'cursor' is an sqlite3.Row.
			### See module 'Database' for the row factory configuration.
			content = [ dict(row) for row in cursor ] if all else dict(cursor)
			if all:
				return content
			else:
				self.__dict__ = dict(cursor)


	### INSERT entry into database
	def db_insert(self):
		database.scrub(self.table)
		#database.scrub_list(self.__dict__.keys())

		db = database.db_open()

		values = [ f":{key}" for key in self.__dict__.keys() ]
		values = ', '.join(values)
		values = '(' + values + ')'

		db.execute(f"INSERT INTO {self.table} {tuple(self.__dict__.keys())} VALUES {values}", self.__dict__)
		db.commit()


	### UPDATE entry in database
	def db_update(self, idd:int):
		database.scrub(self.table)
		database.scrub(str(idd))
		#database.scrub_list(self.__dict__.keys())

		db = database.db_open()

		set_ = [ f"{key} = :{key}" for key in self.__dict__.keys() ]
		set_ = ', '.join(set_)

		update = f"UPDATE {self.table} SET {set_} WHERE id = '{idd}'"

		db.execute(f"{update}", self.__dict__)
		db.commit()


	### DELETE entry in database
	def db_delete(self, id:int):
		database.scrub(self.table)
		database.scrub(str(id))

		db = database.db_open()

		db.execute(f"DELETE FROM {self.table} WHERE id = ?", (id,))
		db.commit()

																	### END CLASS Model


