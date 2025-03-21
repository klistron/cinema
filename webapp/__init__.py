from flask import Flask
from flask_login import (
    LoginManager,
    current_user,
)
from flask_migrate import Migrate

from webapp.db import db
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.main.views import blueprint as main_blueprint


def create_app(config_filename=None):
    app = Flask(__name__)
    
    if config_filename:
        app.config.from_pyfile(config_filename)
    else:
        app.config.from_pyfile("config.py")
        
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
