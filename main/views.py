### CourseWebApp.index
import datetime
import functools
import os

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.exceptions import abort

from main import database
from main import forms
from main import functions
from main import models


bp = Blueprint('index', __name__)


### VIEWS/ROUTES
@bp.route('/')
def index():
	welcomes = models.Model( table='welcome' )
	welcomes.db_select( limit='1', all=True )

	announcements = models.Model( table='announcement' )
	announcements.db_select( join=True, order='created DESC', all=True )

	return render_template('index/index.html', welcomes=welcomes, announcements=announcements)


@bp.route('/welcome', methods=('GET', 'POST'))
@functions.admin_required
def welcome_create():
	welcome = models.Model( table='welcome' )

	form = forms.Formula_Create(
					table='welcome',
					greeting='CKEditor'
					)

	if form.validate_on_submit():
		form.formContent['author_id'] = g.user['id']
		form.formulateContent()

		welcome.__dict__ = form.formContent
		welcome.db_insert()

		flash('Welcome greeting created')
		return redirect(url_for('index'))

	else:
		form.outtakes()

	return render_template('index/welcome.html', welcome=welcome, form=form)


@bp.route('/welcome/update', methods=('GET', 'POST'))
@functions.admin_required
def welcome_update():
	welcome = models.Model( table='welcome' )
	welcome.db_select( where={ 'id': 1} )

	form = forms.Formula_Update( 
				table='welcome',
				greeting=('CKEditor',welcome.greeting) )
	form.formContent = welcome.__dict__
	
	if form.validate_on_submit():
		form.formulateContent()

		welcome.__dict__ = form.formContent
		welcome.db_update(1)

		flash("Welcome greeting updated")
		return redirect(url_for('index'))

	else:
		form.outtakes()

	return render_template('index/update.html', welcome=welcome, form=form)



