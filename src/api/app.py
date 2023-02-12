from flask import Flask
from flask_injector import FlaskInjector
from injector import Injector

from api.dependency_injection import SQLAlchemyModule
from api.exceptions import (AppException, api_exception_handler,
                            app_exception_handler)
from api.extensions import db, migrate, api
from api.config import DefaultConfig
from api.routes.account import AccountsResource, AccountResource
from api.routes.mall import MallsResource, MallResource
from api.routes.unit import UnitsResource, UnitResource


def create_app(config_class: object = DefaultConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)

    app.errorhandler(400)(api_exception_handler)
    app.errorhandler(422)(api_exception_handler)
    app.errorhandler(AppException)(app_exception_handler)

    register_extensions(app)

    return app


def register_extensions(app):
    from api.models.account import Account
    from api.models.mall import Mall
    from api.models.unit import Unit

    api.add_resource(AccountsResource, '/api/accounts/', endpoint='accounts')
    api.add_resource(AccountResource, '/api/accounts/<int:account_id>', endpoint='account')

    api.add_resource(MallsResource, '/api/malls/', endpoint='malls')
    api.add_resource(MallResource, '/api/malls/<int:mall_id>', endpoint='mall')

    api.add_resource(UnitsResource, '/api/units/', endpoint='units')
    api.add_resource(UnitResource, '/api/units/<int:unit_id>', endpoint='unit')

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    injector = Injector([
        SQLAlchemyModule(sqlalchemy_url=app.config.get('SQLALCHEMY_DATABASE_URI'))
    ])
    FlaskInjector(app=app, injector=injector)
