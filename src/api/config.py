import os
from dotenv import load_dotenv


def choose_config_class():
    environment = os.environ.get('FLASK_ENV')

    if environment == 'production':
        return ProductionConfig

    return DevelopmentConfig


def get_config_class(env_filename=None):
    if env_filename:
        load_dotenv(env_filename)

    config_class = choose_config_class()

    for key in dir(config_class):
        if key.isupper() and getattr(config_class, key) is None:
            setattr(config_class, key, os.environ.get(key, None))

    return config_class


class DefaultConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_RECORD_QUERIES = os.environ.get('SQLALCHEMY_RECORD_QUERIES')


class DevelopmentConfig(DefaultConfig):
    pass


class ProductionConfig(DefaultConfig):
    PROPAGATE_EXCEPTIONS = True
