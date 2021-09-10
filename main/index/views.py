""" Module for Index Views """
import datetime
import functools
import os

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from main import forms
from main.auth import decorators
from main.auth.models import User
from main.database import db_session
from main.index.models import Welcome
from main.announcements.models import Announcement


bp = Blueprint('index', __name__)


@bp.route('/')
@decorators.permission_everyone
def index():
    """ View for main.index """
    welcomes = db_session.query(Welcome).limit(1).all()

    announcements = db_session.query(Announcement).join(User).order_by(
            Announcement.created_text.desc()
        ).all()

    announcements_size = len(announcements)

    return render_template('index/index.html', welcomes=welcomes, announcements=announcements, announcements_size=announcements_size)
                                                                ### END Index


@bp.route('/welcome', methods=('GET', 'POST'))
@decorators.permission_professor
def welcome_create():
    """ View for creating Welcome greeting. """
    form = forms.formula_create(
                    table='welcome',
                    greeting='CKEditor' )

    if form.validate_on_submit():
        welcome = Welcome(
            greeting=form.greeting.data,
            author_id=g.user['id'] )
        welcome.save()

        flash('Welcome greeting created')
        return redirect(url_for('index'))

    else:
        form.outtakes()

    return render_template('index/welcome.html', form=form)
                                                                ### END Welcome: Create


@bp.route('/welcome/update', methods=('GET', 'POST'))
@decorators.permission_professor
def welcome_update():
    """ For updating Welcome greeting. """
    welcome = Welcome.query.filter_by(id=1).first()

    form = forms.formula_update( 
                table='welcome',
                greeting=('CKEditor',welcome.greeting) )
    
    if form.validate_on_submit():
        welcome.update( greeting=form.greeting.data )

        flash("Welcome greeting updated")
        return redirect(url_for('index'))

    else:
        form.outtakes()

    return render_template('index/update.html', welcome=welcome, form=form)
                                                                ### END Welcome: Update



