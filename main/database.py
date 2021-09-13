""" Module for database basics """
import click
import os

from flask import _app_ctx_stack
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.exceptions import abort

from config import Config


engine = create_engine( Config.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False} )
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    ),
    scopefunc=_app_ctx_stack.__ident_func__
)

Base = declarative_base()
Base.query = db_session.query_property()


def db_init():
    from main.models import Basic, Model
    from main.announcements.models import Announcement
    from main.auth.models import User
    from main.homework.models import Homework
    from main.index.models import Welcome
    from main.lectures.models import Lecture
    Base.metadata.create_all(bind=engine)


@click.command('db-init')
@with_appcontext
def db_init_command():
    db_init()
    click.echo('Database in the pipe, five by five!')


def app_init(app):
    """ For the Application Factory """
    app.cli.add_command(db_init_command)


