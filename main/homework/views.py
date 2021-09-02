### CourseWebApp.view.homework
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
from main import models
from main.auth import decorators


bp = Blueprint('homework', __name__)


@bp.route('/homework')
@decorators.permission_everyone
def homework_index():
    """ View for Homework index """
    homeworks_proto = models.Model( table='homework' )
    homeworks = homeworks_proto.db_select(
                    join=True,
                    order='homework.id',
                    all=True )

    return render_template('homework/homework.html', homeworks=homeworks)
                                                                ### END Homework Index


@bp.route('/homework/create', methods=('GET','POST'))
@decorators.permission_professor
def homework_create():
    """ View for creating Homework """
    form = forms.formula_create(
                        table='homework',
                        Zahl='Integer',
                        due='String',
                        title='String',
                        keywords='String',
                        file_homework='File',
                        author_id=g.user['id'] )

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
                                                                ### END Homework: Create


@bp.route('/homework/<int:id>/update', methods=('GET', 'POST'))
@decorators.permission_TA
def homework_update(id):
    """ View for updating Homework """
    homework = models.Model( table='homework' )
    homework.db_select( where={'id':id} )

    form = forms.formula_update(
                    table='homework',
                    Zahl=('Integer',homework.Zahl),
                    due=('String',homework.due),
                    title=('String',homework.title),
                    keywords=('String',homework.keywords),
                    file_homework=('File',None) )
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
                                                                ### END Homework: Update


@bp.route('/homework/<int:id>/delete', methods=('POST',))
@decorators.permission_professor
def homework_delete(id):
    """ View for deleting Homework """
    homework = models.Model( table='homework' )
    homework.db_select( where={'id':id} )
    homework.db_delete(id)

    flash(f"Homework {id} successfully deleted")
    return redirect(url_for('homework.homework_index'))
                                                                ### END Homework: Delete

