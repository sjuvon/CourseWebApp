""" Module for Authentication Views """
import sqlite3

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from main import database
from main.auth import forms, models


bp = Blueprint('auth', __name__)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """ View for registering accounts """
    form = forms.Register()

    if form.validate_on_submit():
        register = models.User(
            username=form.username.data,
            password=form.password.data )
        register.save()

        flash('Account successfully created')
        return redirect(url_for('auth.login'))

    else:
        form.outtakes()

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET','POST'))
def login():
    """ View for logging in """
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
        #### Gross :(
        g.user = vars(models.User.query.filter_by(username=username).first())


@bp.route('/logout')
def logout():
    """ View for logging out """
    session.clear()
    flash('Logged out.  Goodbye!')
    return redirect(url_for('index'))



