from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager


db = SQLAlchemy()

# login_manager = LoginManager()


def register_blueprints(app):
    from .customer import bp as customer_bp
    app.register_blueprint(customer_bp)


def register_plugin(app):
    # login_manager.init_app(app)
    db.init_app(app)


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')

    register_blueprints(app)

    register_plugin(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()
