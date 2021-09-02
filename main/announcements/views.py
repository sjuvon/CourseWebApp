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
from main import models
from main.auth import decorators


bp = Blueprint('announcements', __name__)


@bp.route('/announcements/create', methods=('GET','POST'))
@decorators.permission_TA
def announcements_create():
    """ View creating Announcements. """
    form = forms.formula_create(
                    table='announcement',
                    subject='String',
                    body='TextArea',
                    author_id=g.user['id'] )

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
                                                                ### END Announcement: Create


@bp.route('/announcements/<int:id>/update', methods=('GET', 'POST'))
@decorators.permission_TA
def announcements_update(id):
    """ View for updating Announcements. """
    announcement = models.Model( table='announcement' )
    announcement.db_select(
                        where={ 'id': id } )

    form = forms.formula_update(
                    table='announcement',
                    subject=('String',announcement.subject),
                    body=('TextArea',announcement.body) )
    
    form.formContent = announcement.__dict__

    if form.validate_on_submit():
        form.formContent['updated_text'] = datetime.datetime.now().astimezone().strftime('%d %b %Y at %H:%M %Z')
        form.formulateContent()
        
        announcement.__dict__ = form.formContent
        announcement.db_update(id)

        flash('Announcement successfully updated')
        return redirect(url_for('index'))

    else:
        form.outtakes()

    return render_template('announcements/update.html', announcement=announcement, form=form)
                                                                ### END Announcement: Update


@bp.route('/announcements/<int:id>/delete', methods=('POST',))
@decorators.permission_TA
def announcements_delete(id):
    """ View for deleting Announcements. """
    announcement = models.Model( table='announcement' )
    announcement.db_select( where={ 'id':id } )
    announcement.db_delete(id)

    flash('Announcement successfully deleted')
    return redirect(url_for('index'))
                                                                ### END Announcement: Delete


