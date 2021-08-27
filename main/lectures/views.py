### CourseWebApp.lectures
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


bp = Blueprint('lectures', __name__)


### VIEWS/ROUTES
### Lectures index
@bp.route('/lectures')
def lectures_index():
	lectures_proto = models.Model( table='lecture' )
	lectures = lectures_proto.db_select( join=True, order='lecture.id', all=True )

	### Gadget for webpage aesthetic.
	### See BLOCK: CONTENT in lectures.html
	Max = database.db_query(
				'lecture',
				what='MAX(week)'
				)

	M = 0 if Max[0] is None else Max[0]
	###

	return render_template('lectures/lectures.html', lectures=lectures, M=M)


### Create lecture
@bp.route('/lectures/create', methods=('GET','POST'))
@functions.admin_required
def lectures_create():
	form = forms.Formula_Create(
					table='lecture',
					week='Integer',
					Zahl='Integer',
					day='String',
					title='String',
					summary='TextArea',
					file_lecture='File',
					author_id=g.user['id']
					)

	if form.validate_on_submit():
		form.formContent['id'] = form.Zahl.data
		form.formulateContent()

		lecture = models.Model( table='lecture' )
		lecture.__dict__ = form.formContent
		lecture.db_insert()

		flash(f"Lecture {form.Zahl.data} successfully created")
		return redirect(url_for('lectures.lectures_index'))

	else:
		form.outtakes()

	return render_template('lectures/create.html', form=form)


### Update lecture
@bp.route('/lectures/<int:id>/update', methods=('GET','POST'))
@functions.admin_required
def lectures_update(id):
	lecture = models.Model( table='lecture' )
	lecture.db_select( where={'id':id} )

	form = forms.Formula_Update(
					table='lecture',
					week=('Integer',lecture.week),
					Zahl=('Integer',lecture.Zahl),
					day=('String',lecture.day),
					title=('String',lecture.title),
					summary=('TextArea',lecture.summary),
					file_lecture=('File',None)
					)
	form.formContent = lecture.__dict__

	if form.validate_on_submit():
		form.formulateContent()

		lecture.__dict__ = form.formContent
		lecture.db_update(id)

		flash(f"Lecture {form.Zahl.data} successfully updated")
		return redirect(url_for('lectures.lectures_index'))

	else:
		form.outtakes()

	return render_template('lectures/update.html', lecture=lecture, form=form)


### Delete lecture
@bp.route('/lectures/<int:id>/delete', methods=('POST',))
@functions.admin_required
def lectures_delete(id):
	lecture = models.Model( table='lecture' )
	lecture.db_select( where={'id':id} )
	lecture.db_delete(id)

	flash(f"Lecture {id} successfully deleted")
	return redirect(url_for('lectures.lectures_index'))

