### CourseWebApp.auth.decorators
""" Module for decorators for role-based views. """

import functools

from flask import g
from flask import redirect
from flask import url_for
from werkzeug.exceptions import abort

from main.auth import views


def permission_everyone(view):
    """ Decorator for role-based view: Everyone """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        ### This view is free for everyone to see
        return view(**kwargs)
    return wrapped_view


def permission_student(view):
    """ Decorator for role-based view: Student """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


def permission_grader(view):
    """ Decorator for role-based view: Grader """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        elif g.user['role_id'] < 2:
            abort(403)
        return view(**kwargs)
    return wrapped_view


def permission_TA(view):
    """ Decorator for role-based view: Teaching Assistant """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        elif g.user['role_id'] < 3:
            abort(403)
        return view(**kwargs)
    return wrapped_view


def permission_professor(view):
    """ Decorator for role-based view: Professor """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        elif g.user['role_id'] < 4:
            abort(403)
        return view(**kwargs)
    return wrapped_view


"""
### Login requirement decorator
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
    

### Admin requirement decorator
def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user['username'] != 'admin':         
            abort(403)
        return view(**kwargs)
    return wrapped_view"""