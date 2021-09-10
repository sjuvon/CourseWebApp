""" Module for Lecture Views """
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from main import forms, uploads
from main.auth import decorators
from main.auth.models import User
from main.database import db_session
from main.lectures import models


bp = Blueprint('lectures', __name__)


@bp.route('/lectures')
@decorators.permission_everyone
def lectures_index():
    """ View for Lectures index """
    lectures = db_session.query(models.Lecture).join(User).all()

    ### Gadget for webpage aesthetic.
    ### See BLOCK: CONTENT in lectures.html
    try:
        M = max([lecture.week for lecture in lectures])
    except:
        M = 0

    return render_template('lectures/lectures.html', lectures=lectures, M=M)
                                                                ### END Lectures Index


@bp.route('/lectures/create', methods=('GET','POST'))
@decorators.permission_professor
def lectures_create():
    """ View for creating Lectures """
    form = forms.formula_create(
                    table='lecture',
                    week='Integer',
                    Zahl='Integer',
                    day='String',
                    title='String',
                    summary='TextArea',
                    file_lecture='File' )

    if form.validate_on_submit():
        filename = uploads.upload(form.file_lecture.data, 'lectures')
        lecture = models.Lecture(
            id=form.Zahl.data,
            Zahl=form.Zahl.data,
            week=form.week.data,
            day=form.day.data,
            title=form.title.data,
            summary=form.summary.data,
            file_lecture=filename,
            author_id=g.user['id'] )
        lecture.save()

        flash(f"Lecture {form.Zahl.data} successfully created")
        return redirect(url_for('lectures.lectures_index'))

    else:
        form.outtakes()

    return render_template('lectures/create.html', form=form)
                                                                ### END Lectures: Create


@bp.route('/lectures/<int:id>/update', methods=('GET','POST'))
@decorators.permission_professor
def lectures_update(id):
    """ View for updating Lectures """
    lecture = models.Lecture.query.filter_by(id=id).first()

    form = forms.formula_update(
                    table='lecture',
                    id=id,
                    week=('Integer',lecture.week),
                    Zahl=('Integer',lecture.Zahl),
                    day=('String',lecture.day),
                    title=('String',lecture.title),
                    summary=('TextArea',lecture.summary),
                    file_lecture=('File',None) )

    if form.validate_on_submit():
        filename = uploads.upload(form.file_lecture.data, 'lectures')
        lecture.update(
            id=form.Zahl.data,
            Zahl=form.Zahl.data,
            week=form.week.data,
            day=form.day.data,
            title=form.title.data,
            summary=form.summary.data,
            file_lecture=filename )

        flash(f"Lecture {form.Zahl.data} successfully updated")
        return redirect(url_for('lectures.lectures_index'))

    else:
        form.outtakes()

    return render_template('lectures/update.html', lecture=lecture, form=form)
                                                                ### END Lectures: Update


@bp.route('/lectures/<int:id>/delete', methods=('POST',))
@decorators.permission_professor
def lectures_delete(id):
    """ View for deleting Lectures """
    lecture = models.Lecture.query.filter_by(id=id).first()
    lecture.delete()

    flash(f"Lecture {id} successfully deleted")
    return redirect(url_for('lectures.lectures_index'))
                                                                ### END Lectures: Delete


