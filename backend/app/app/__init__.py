from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

login_manager = LoginManager()


def register_blueprints(app):
    from .user.routes import bp as user_bp
    app.register_blueprint(user_bp)


def register_plugin(app):
    login_manager.init_app(app)
    db.init_app(app)


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.config')

    register_blueprints(app)

    register_plugin(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()
