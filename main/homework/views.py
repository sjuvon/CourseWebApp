""" Module for Homework Views """
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from main import forms, uploads
from main.auth import decorators
from main.auth.models import User
from main.database import db_session
from main.homework import models


bp = Blueprint('homework', __name__)


@bp.route('/homework')
@decorators.permission_everyone
def homework_index():
    """ View for Homework index """
    homeworks = models.Homework.query.join(User).all()

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
                        file_homework='File' )

    if form.validate_on_submit():
        filename = uploads.upload(form.file_homework.data, 'homework')

        homework = models.Homework(
            id=form.Zahl.data,
            Zahl=form.Zahl.data,
            due=form.due.data,
            title=form.title.data,
            keywords=form.keywords.data,
            file_homework=filename,
            author_id=g.user['id'] )
        homework.save()

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
    homework = models.Homework.query.filter_by(id=id).first()

    form = forms.formula_update(
                    table='homework',
                    id=id,
                    Zahl=('Integer',homework.Zahl),
                    due=('String',homework.due),
                    title=('String',homework.title),
                    keywords=('String',homework.keywords),
                    file_homework=('File',None) )

    if form.validate_on_submit():
        filename = uploads.upload(form.file_homework.data, 'homework')
        homework.update(
            id=form.Zahl.data,
            Zahl=form.Zahl.data,
            due=form.due.data,
            title=form.title.data,
            keywords=form.keywords.data,
            file_homework=filename )

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
    homework = models.Homework.query.filter_by(id=id).first()
    homework.delete()

    flash(f"Homework {id} successfully deleted")
    return redirect(url_for('homework.homework_index'))
                                                                ### END Homework: Delete

