import os

from injector import Binder, Module, singleton
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.services.account import AccountService
from api.repositories.account import AccountRepository


class SQLAlchemyModule(Module):
    def __init__(self, sqlalchemy_url: str):
        self.sqlalchemy_url = sqlalchemy_url

    def configure(self, binder: Binder):
        session = sessionmaker(
            create_engine(self.sqlalchemy_url),
            expire_on_commit=False
        )
        binder.bind(interface=sessionmaker, to=session, scope=singleton)
        binder.bind(interface=AccountService, to=AccountService, scope=singleton)
        binder.bind(interface=AccountRepository, to=AccountRepository, scope=singleton)
