### CourseWebApp.view.index
import datetime
import functools
import os

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


bp = Blueprint('index', __name__)


@bp.route('/')
@decorators.permission_everyone
def index():
    """ View for main.index """
    welcomes_proto = models.Model( table='welcome' )
    welcomes = welcomes_proto.db_select(
                    limit='1',
                    all=True )

    announcements_proto = models.Model( table='announcement' )
    announcements = announcements_proto.db_select(
                        join=True,
                        order='created DESC',
                        all=True )

    announcements_size = len(announcements)

    return render_template('index/index.html', welcomes=welcomes, announcements=announcements, announcements_size=announcements_size)
                                                                ### END Index


@bp.route('/welcome', methods=('GET', 'POST'))
@decorators.permission_professor
def welcome_create():
    """ View for creating Welcome greeting. """
    welcome = models.Model( table='welcome' )

    form = forms.formula_create(
                    table='welcome',
                    greeting='CKEditor' )

    if form.validate_on_submit():
        form.formContent['author_id'] = g.user['id']
        form.formulateContent()

        welcome.__dict__ = form.formContent
        welcome.db_insert()

        flash('Welcome greeting created')
        return redirect(url_for('index'))

    else:
        form.outtakes()

    return render_template('index/welcome.html', welcome=welcome, form=form)
                                                                ### END Welcome: Create


@bp.route('/welcome/update', methods=('GET', 'POST'))
@decorators.permission_professor
def welcome_update():
    """ For updating Welcome greeting. """
    welcome = models.Model( table='welcome' )
    welcome.db_select( where={'id': 1} )

    form = forms.formula_update( 
                table='welcome',
                greeting=('CKEditor',welcome.greeting) )
    form.formContent = welcome.__dict__
    
    if form.validate_on_submit():
        form.formulateContent()

        welcome.__dict__ = form.formContent
        welcome.db_update(1)

        flash("Welcome greeting updated")
        return redirect(url_for('index'))

    else:
        form.outtakes()

    return render_template('index/update.html', welcome=welcome, form=form)
                                                                ### END Welcome: Update



