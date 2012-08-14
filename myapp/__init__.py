import os
import logging

from flask import Flask, render_template, abort
from sqlalchemy import create_engine
from flask.ext.login import LoginManager
from flaskext.bcrypt import Bcrypt
from flaskext.openid import OpenID
from flaskext.script import Manager
from flask.ext.assets import Environment, Bundle

from .database import init_engine, init_db, db_session
from .models import User, bcrypt
from .utils import q

from .home.views import mod as main_blueprint
from .users.views import mod as user_blueprint, oid


login_manager = LoginManager()
assets = Environment()



def create_app(db_uri='any'):

    app = Flask(__name__)
    app.config.from_object('myapp.config')
    app.config.from_pyfile(os.path.join(app.instance_path, 'config.py'))
    if db_uri == 'Test':
        init_engine(app.config['TEST_DATABASE_URL'])
    else:
        init_engine(app.config['DATABASE_URL'])
    #Register Blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint, url_prefix="/users")

    app.logger.setLevel(logging.WARNING)
    logger_handler = logging.FileHandler(os.path.join(app.config['LOG_LOCATION'],
                                                      'app_errors.log'))
    formatter = logging.Formatter('%(asctime)s  %(levelname)s - %(message)s'
                              ' [in %(pathname)s:%(lineno)d]')
    logger_handler.setFormatter(formatter)
    app.logger.addHandler(logger_handler)


    @app.teardown_request
    def shutdown_session(exception=None):
        db_session.remove()

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')

    @app.errorhandler(500)
    def internal_error(exception):
        app.logger.exception(exception)
        return "Some Internal error has taken place."


    bcrypt.init_app(app)
    login_manager.setup_app(app)
    login_manager.login_view = 'users.login'
    assets.init_app(app)

    css = Bundle('base.css', 'content.css')
    assets.register('css_all', css)
    
    return app


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
