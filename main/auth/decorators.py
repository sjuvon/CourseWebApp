"""
    Module for setting role-based Views.

    Upon registration, every user is assigned one of four
    roles and role IDs:
          'Student'  <~~~>  1 (Default)
           'Grader'  <~~~>  2
               'TA'  <~~~>  3
        'Professor'  <~~~>  4
    Users then have access to a particular View based on
    their role. The hierarchy is set so that every role
    has the permissions of its predecessor.
"""
import functools

from flask import g, redirect, url_for
from werkzeug.exceptions import abort

from main.auth import views


def permission_everyone(view):
    """ Decorator for role-based view: Everyone """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        ### This View is free for everyone to see.
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


