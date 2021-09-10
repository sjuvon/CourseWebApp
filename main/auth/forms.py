""" Module for Authentication Forms """
import sqlite3

from flask import flash, g
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from main import database
from main.auth import models


class Register(FlaskForm):
    """ Registration form """
    username = StringField(
        'Username',validators=[DataRequired(), Length(min=3, message='Username must have at least %(min)d characters')])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=4, message='Password must have at least %(min)d characters')])
    password_confirm = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField(label=('Register'))


    def validate_username(self,username):
        query = models.User.query.filter_by(username=self.username.data).first()

        if query is not None:
            raise ValidationError(
                f"Username {self.username.data} is unavailable")

    def outtakes(self):
        if self.errors:
            for error in self.errors.values():
                flash(*error)
                                                                            ### END Registration Form


class Login(FlaskForm):
    """ Login form """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField(label=('Submit'))


    def validate_username(self,username):
        user = models.User.query.filter_by(username=self.username.data).first()
        
        if user is None:
            raise ValidationError(
                f"Username {self.username.data} does not exist")
        elif not check_password_hash(user.password, self.password.data):
            raise ValidationError("Incorrect password")

    def outtakes(self):
        if self.errors:
            for error in self.errors.values():
                flash(*error)
                                                                            ### END Login Form

    