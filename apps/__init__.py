# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from flask import Flask
from flask_modals import Modal
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy, Pagination
from importlib import import_module
from apps.utils.stocks_properties import read_properties_file


db = SQLAlchemy()
login_manager = LoginManager()
print('El path de la aplicacion es : ',__path__)
props = read_properties_file('finanzas.properties')
sql_scripts = read_properties_file('sql_scripts.properties')


def register_extensions(app):
    db.init_app(app)
    print('1 Register extension')
    login_manager.init_app(app)


def register_blueprints(app):
    print('1 Register blueprints')
    for module_name in ('authentication', 'home', 'masterplan', 'organizations'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        print('3 configure database')
        try:
            print('#### Creando la base de datos ####')
            db.create_all()
            #from . import db
            #db.init_app(app)
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove() 


def create_app(config):
    print('4 Create app')
    app = Flask(__name__)
    modal = Modal(app)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
