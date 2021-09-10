""" Module for Announcement Views """
import datetime

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from main import forms
from main.auth import models
from main.announcements import models
from main.auth import decorators


bp = Blueprint('announcements', __name__)


@bp.route('/announcements/create', methods=('GET','POST'))
@decorators.permission_TA
def announcements_create():
    """ View creating Announcements. """
    form = forms.formula_create(
                    table='announcement',
                    subject='String',
                    body='TextArea' )

    if form.validate_on_submit():
        announcement = models.Announcement(
                            subject=form.subject.data,
                            body=form.body.data,
                            created_text=datetime.datetime.now().astimezone().strftime('%d %b %Y at %H:%M %Z'),
                            author_id=g.user['id'] )
        announcement.save()

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
    announcement = models.Announcement.query.filter_by(id=id).first()

    form = forms.formula_update(
                    table='announcement',
                    subject=('String',announcement.subject),
                    body=('TextArea',announcement.body) )

    if form.validate_on_submit():        
        announcement.update(
            subject=form.subject.data,
            body=form.body.data,
            updated_text=datetime.datetime.now().astimezone().strftime('%d %b %Y at %H:%M %Z') )

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
    announcement = models.Announcement.query.filter_by(id=id).first()
    announcement.delete()

    flash('Announcement successfully deleted')
    return redirect(url_for('index'))
                                                                ### END Announcement: Delete


