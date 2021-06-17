import os
from flask import Flask
from flask_bootstrap import Bootstrap
from webapp.main.routes import main
from webapp.errors.handlers import errors

bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)

    # Enable bootstrap
    bootstrap.init_app(app)

    # Setup blueprints
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # Set secret key
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    return app
