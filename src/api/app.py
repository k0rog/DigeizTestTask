from flask import Flask
from flask_injector import FlaskInjector
from flask_restful import Api
from injector import Injector

from api.dependency_injection import SQLAlchemyModule
from api.exceptions import (AppException, api_exception_handler,
                            app_exception_handler)
from api.extensions import db, migrate
from api.routes.account import AccountsResource, AccountResource
from api.config import DefaultConfig


api = Api()


def create_app(config_class: object = DefaultConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)

    api.add_resource(AccountsResource, '/api/accounts/', endpoint='accounts')
    api.add_resource(AccountResource, '/api/accounts/<int:account_id>', endpoint='account')
    api.init_app(app)

    app.errorhandler(400)(api_exception_handler)
    app.errorhandler(422)(api_exception_handler)
    app.errorhandler(AppException)(app_exception_handler)

    register_extensions(app)

    return app


def register_extensions(app):
    from api.models.account import Account
    from api.models.mall import Mall
    from api.models.unit import Unit

    db.init_app(app)
    migrate.init_app(app, db)

    injector = Injector([
        SQLAlchemyModule(sqlalchemy_url=app.config.get('SQLALCHEMY_DATABASE_URI'))
    ])
    FlaskInjector(app=app, injector=injector)


