### CourseWebApp.auth
import sqlite3

from flask import flash
from flask import g
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import ValidationError

from main import database
from main import models


### Registration form
class Register(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=3, message='Username must have at least %(min)d characters')])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=4, message='Password must have at least %(min)d characters')])
    password_confirm = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField(label=('Register'))

    formContent = { 'username': None, 'password': None }
    def formulateContent(self):
        self.formContent['username'] = self.username.data
        self.formContent['password'] = generate_password_hash(self.password.data)


    def validate_username(self,username):

        database.scrub(self.username.data)
        query = database.db_query('user', join=False, where={ 'username': self.username.data }, all=False)

        if query is not None:
            raise ValidationError(
                f"Username {self.username.data} is unavailable")

    def outtakes(self):
        if self.errors:
            for error in self.errors.values():
                flash(*error)
                                                                            ### END Registration Form


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField(label=('Submit'))


    def validate_username(self,username):

        database.scrub(self.username.data)
        user = database.db_query('user', join=False, where={ 'username': self.username.data }, all=False)
        
        if user is None:
            raise ValidationError(
                f"Username {self.username.data} does not exist")
        elif not check_password_hash(user['password'], self.password.data):
            raise ValidationError("Incorrect password")

    def outtakes(self):
        if self.errors:
            for error in self.errors.values():
                flash(*error)
                                                                            ### END Login Form

    