### CourseWebApp.announcements
import datetime

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


### 20 AUG 2021: MAKE A close-all BUTTON FOR ANNOUNCEMENTS

bp = Blueprint('announcements', __name__)


### VIEWS/ROUTES
### Create announcement
@bp.route('/announcements/create', methods=('GET','POST'))
@functions.admin_required
def announcements_create():
	form = forms.Formula_Create(
					table='announcement',
					subject='String',
					body='TextArea',
					author_id=g.user['id']
					)

	if form.validate_on_submit():
		form.formContent['created_text'] = datetime.datetime.now().astimezone().strftime('%d %b %Y at %H:%M %Z')
		form.formulateContent()

		announcement = models.Model( table='announcement' )
		announcement.__dict__ = form.formContent
		announcement.db_insert()

		flash('Announcement successfully posted')
		return redirect(url_for('index'))
	
	else:
		form.outtakes()

	return render_template('announcements/create.html', form=form)


### Update announcement
@bp.route('/announcements/<int:id>/update', methods=('GET', 'POST'))
@functions.admin_required
def announcements_update(id):
	### Initialise announcement to update
	announcement = models.Model( table='announcement' )
	announcement.db_select(
						where={ 'id': id }
						)
	### Initialise form
	form = forms.Formula_Update(
					table='announcement',
					subject=('String',announcement.subject),
					body=('TextArea',announcement.body)
					)
	### Hand off database data to form
	form.formContent = announcement.__dict__

	if form.validate_on_submit():
		### Prepare form for database entry
		form.formContent['updated'] = datetime.datetime.now().astimezone().strftime('%d %b %Y at %H:%M %Z')
		form.formulateContent()
		
		### Hand off user input to model for final database update
		announcement.__dict__ = form.formContent
		announcement.db_update(id)

		flash('Announcement successfully updated')
		return redirect(url_for('index'))

	else:
		form.outtakes()

	return render_template('announcements/update.html', announcement=announcement, form=form)


### Delete announcement
@bp.route('/announcements/<int:id>/delete', methods=('POST',))
@functions.admin_required
def announcements_delete(id):
	announcement = models.Model( table='announcement' )
	announcement.db_select( where={ 'id':id } )
	announcement.db_delete(id)

	flash('Announcement successfully deleted')
	return redirect(url_for('index'))



