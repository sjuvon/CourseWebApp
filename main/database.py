### CourseWebApp.database

import click
import os
import sqlite3

from flask import current_app
from flask import g
from flask.cli import with_appcontext

from werkzeug.exceptions import abort


### Connect to SQLite database
def db_open():
	if 'db' not in g:
		g.db = sqlite3.connect(
					current_app.config['DATABASE'],
					detect_types=sqlite3.PARSE_DECLTYPES)
		g.db.row_factory = sqlite3.Row
	return g.db


### Close database connection
def db_close(e=None):
	db = g.pop('db', None)
	if db is not None:
		db.close()


### Towards initialising the database
def db_init():
	db = db_open()
	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))


### Initialise database in command-line
@click.command('db-init')
@with_appcontext
def db_init_command():
	### N.B. This will clear existing database and establish new one
	db_init()
	click.echo('Database in the pipe, five by five!')


### For the Application Factory
def app_init(app):
	app.teardown_appcontext(db_close)
	app.cli.add_command(db_init_command)


### To sanitise user inputs
### for database entry.
def scrub(string,special=False):
	if special:
		S = { '"', "'", ";" }
		for x in string:
			if x in S:
				abort(400)
		
	elif not string.isalnum():
		abort(400)

def scrub_list(arr):
	for entry in arr:
		scrub(entry)

def scrub_dict(dictionary):
	for key, value in dictionary.items():
		scrub(key)

		if key == 'table':
			scrub(value)
		elif type(value) == str:
			scrub(value,special=True)
		else:
			pass


### QUERY (SELECT) entry from database
def db_query(table:str, what:str='*', join=False, where:dict=None, order:str=None, limit:str=None, all=False):
	scrub_dict(locals())

	db = db_open()

	"""
	The following is to build:
	query = f'SELECT {what} FROM {self.table} JOIN user ON {self.table}.author_id = user.id WHERE {where} ORDER BY {order} LIMIT {limit}'
																																	"""

	query = f"SELECT {what} FROM {table}"
	if join:
		query = query + f" JOIN user ON {table}.author_id = user.id"		
	if where:
		wo = [ f"{table}.{key} = :{key}" for key in where.keys() ]
		wo = ' AND '.join(wo)
		query = query + f" WHERE {wo}"
	if order:
		query = query + f" ORDER BY {order}"
	if limit:
		query = query + f" LIMIT {limit}"

	if where:
		return db.execute(query, where).fetchall() if all else db.execute(query, where).fetchone()
	else:
		return db.execute(query).fetchall() if all else db.execute(query).fetchone()


