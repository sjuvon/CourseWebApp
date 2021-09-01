### CourseWebApp.auth
import sqlite3

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
from main import models
from main.auth import forms


bp = Blueprint('auth', __name__)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """ View for registering accounts """
    form = forms.Register()

    if form.validate_on_submit():
        form.formulateContent()

        register = models.Model( table='user' )
        register.__dict__ = form.formContent
        register.db_insert()

        flash('Account successfully created')
        return redirect(url_for('auth.login'))

    else:
        form.outtakes()

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET','POST'))
def login():
    """ View for login """
    form = forms.Login()

    if form.validate_on_submit():
        session.clear()
        session['username'] = form.username.data
        flash(f'Logged in.  Welcome, {form.username.data}!')
        return redirect(url_for('index'))

    else:
        form.outtakes()

    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')
    if username is None:
        g.user = None
    else:
        g.user = database.db_query(
                    'user',
                    join=False,
                    where={'username':username},
                    all=False )


@bp.route('/logout')
def logout():
    """ View for logging out """
    session.clear()
    flash('Logged out.  Goodbye!')
    return redirect(url_for('index'))



