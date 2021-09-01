### CourseWebApp.view.lectures
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


bp = Blueprint('lectures', __name__)


@bp.route('/lectures')
@decorators.permission_everyone
def lectures_index():
    """ View for Lectures index """
    lectures_proto = models.Model( table='lecture' )
    lectures = lectures_proto.db_select(
                    join=True,
                    order='lecture.id',
                    all=True )

    """ Gadget for webpage aesthetic. (See BLOCK: CONTENT in lectures.html) """
    Max = database.db_query(
                'lecture',
                what='MAX(week)' )

    M = 0 if Max[0] is None else Max[0]

    return render_template('lectures/lectures.html', lectures=lectures, M=M)
                                                                ### END Lectures Index


@bp.route('/lectures/create', methods=('GET','POST'))
@decorators.permission_professor
def lectures_create():
    """ For creating Lectures """
    form = forms.formula_create(
                    table='lecture',
                    week='Integer',
                    Zahl='Integer',
                    day='String',
                    title='String',
                    summary='TextArea',
                    file_lecture='File',
                    author_id=g.user['id'] )

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
                                                                ### END Lectures: Create


@bp.route('/lectures/<int:id>/update', methods=('GET','POST'))
@decorators.permission_professor
def lectures_update(id):
    """ For updating Lectures """
    lecture = models.Model( table='lecture' )
    lecture.db_select( where={'id':id} )

    form = forms.formula_update(
                    table='lecture',
                    week=('Integer',lecture.week),
                    Zahl=('Integer',lecture.Zahl),
                    day=('String',lecture.day),
                    title=('String',lecture.title),
                    summary=('TextArea',lecture.summary),
                    file_lecture=('File',None) )
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
                                                                ### END Lectures: Update


@bp.route('/lectures/<int:id>/delete', methods=('POST',))
@decorators.permission_professor
def lectures_delete(id):
    """ For deleting Lectures """
    lecture = models.Model( table='lecture' )
    lecture.db_select( where={'id':id} )
    lecture.db_delete(id)

    flash(f"Lecture {id} successfully deleted")
    return redirect(url_for('lectures.lectures_index'))
                                                                ### END Lectures: Delete


