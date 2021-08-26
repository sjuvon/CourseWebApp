### CourseWebApp.homework
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


bp = Blueprint('homework', __name__)


### VIEWS/ROUTES
### Homework index
@bp.route('/homework')
def homework_index():
	homeworks = models.Model( table='homework' )
	homeworks.db_select( join=True, order='homework.id', all=True )
	return render_template('homework/homework.html', homeworks=homeworks)


### Create homework
@bp.route('/homework/create', methods=('GET','POST'))
@functions.admin_required
def homework_create():
	form = forms.Formula_Create(
						table='homework',
						Zahl='Integer',
						due='String',
						title='String',
						keywords='String',
						file_homework='File',
						update_='Gotta get rid of this',
						author_id=g.user['id']
						)

	if form.validate_on_submit():
		form.formContent['id'] = form.Zahl.data
		form.formulateContent()

		homework = models.Model( table='homework' )
		homework.__dict__ = form.formContent
		homework.db_insert()

		flash(f"Homework {form.Zahl.data} successfully created")
		return redirect(url_for('homework.homework_index'))

	else:
		form.outtakes()

	return render_template('homework/create.html', form=form)


### Update homework
@bp.route('/homework/<int:id>/update', methods=('GET', 'POST'))
@functions.admin_required
def homework_update(id):
	homework = models.Model( table='homework' )
	homework.db_select( where={'id':id} )

	form = forms.Formula_Update(
					table='homework',
					Zahl=('Integer',homework.Zahl),
					due=('String',homework.due),
					title=('String',homework.title),
					keywords=('String',homework.keywords),
					file_homework=('File',None)
					)
	form.formContent = homework.__dict__

	if form.validate_on_submit():
		form.formulateContent()

		homework.__dict__ = form.formContent
		homework.db_update(id)

		flash(f"Homework {id} successfully updated")
		return redirect(url_for('homework.homework_index'))

	else:
		form.outtakes()

	return render_template('homework/update.html', homework=homework, form=form)


### Delete homework
@bp.route('/homework/<int:id>/delete', methods=('POST',))
@functions.admin_required
def homework_delete(id):
	homework = models.Model( table='homework' )
	homework.db_select( where={'id':id} )
	homework.db_delete(id)

	flash(f"Homework {id} successfully deleted")
	return redirect(url_for('homework.homework_index'))


