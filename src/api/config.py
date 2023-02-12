import os


def get_config_class():
    environment = os.environ.get('ENVIRONMENT')

    if environment == 'production':
        return ProductionConfig

    return DevelopmentConfig


class DefaultConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_RECORD_QUERIES = os.environ.get('SQLALCHEMY_RECORD_QUERIES')


class DevelopmentConfig(DefaultConfig):
    pass


class ProductionConfig(DefaultConfig):
    pass
