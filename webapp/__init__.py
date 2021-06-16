from flask import Flask
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    bootstrap.init_app(app)
    from webapp.main.routes import main
    from webapp.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(errors)

    import os
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    return app
