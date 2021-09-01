### CourseWebApp.app
"""
    Main app module containing the Application Factory
"""

import os
import random

from flask import Flask
from flask_ckeditor import CKEditor

from config import Config

from main import database
from main.announcements.views import bp as bp_announcements
from main.auth.views import bp as bp_auth
from main.homework.views import bp as bp_homework
from main.lectures.views import bp as bp_lectures
from main.views import bp as bp_index


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    CKEditor().init_app(app)

    database.app_init(app)
    register_blueprints(app)

    @app.before_request
    def vor():
        database.db_open()

    @app.after_request
    def nach(response):
        database.db_close()
        return response


    ### Signs of life
    @app.route('/gg')
    def hello():
        quotes = [
            "My life for Aiur!",
            "Issah'tu!",
            "Gee'hous!",
            "Gau'gurah!",
            "Khas I serve!",
            "Honour guide me!", 
            "Adun Toridas!",
            "En Taro Adun!",
            "Power overwhelming!",
            "You must construct additional pylons",
            "SCV good to go, sir!",
            "Reportin' for duty!",
            "I can't build it---somethin's in the way!",
            "Jacked up and good to go!",
            "Go, go, go!",
            "Can I take your order?",
            "Destination?",
            "Input coordinates",
            "Hang on, we're in for some chop!",
            "Ab-so-lutely!"]
        return random.choices(quotes).pop()
        

    return app


def register_blueprints(app):
    app.register_blueprint(bp_index)
    app.add_url_rule('/', endpoint='index')

    app.register_blueprint(bp_auth, url_prefix='/auth')
    app.register_blueprint(bp_announcements)
    app.register_blueprint(bp_homework)
    app.register_blueprint(bp_lectures)


