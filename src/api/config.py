import os
from dotenv import load_dotenv


def choose_config_class():
    environment = os.environ.get('ENVIRONMENT')

    if environment == 'production':
        return ProductionConfig

    return DevelopmentConfig


def get_config_class(env_filename=None):
    if env_filename:
        load_dotenv(env_filename)

    config_class = choose_config_class()

    for key in dir(config_class):
        if key.isupper():
            setattr(config_class, key, os.environ.get(key, None))

    return config_class


class DefaultConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_RECORD_QUERIES = os.environ.get('SQLALCHEMY_RECORD_QUERIES')


class DevelopmentConfig(DefaultConfig):
    pass


class ProductionConfig(DefaultConfig):
    pass
