import pytest

from sqlalchemy.orm import sessionmaker
from testing.postgresql import Postgresql
from sqlalchemy import create_engine

from api.app import create_app

from api.repositories.account import AccountRepository
from api.repositories.mall import MallRepository
from api.repositories.unit import UnitRepository
from api.services.account import AccountService
from api.services.mall import MallService
from api.services.unit import UnitService

from api.extensions import db as _db
from api.config import get_config_class


@pytest.fixture(scope='session')
def sqlalchemy_database_url():
    with Postgresql() as in_memory_postgres:
        dsn = in_memory_postgres.dsn()
        database_url = 'postgresql://{}@{}:{}/{}'.format(
            dsn['user'], dsn['host'], dsn['port'], dsn['database']
        )

        yield database_url


@pytest.fixture(scope='session')
def app(sqlalchemy_database_url):

    config_class = get_config_class('.env.test')
    config_class.SQLALCHEMY_DATABASE_URI = sqlalchemy_database_url

    app = create_app(config_class)

    app.config.update({
        'TESTING': True,
    })

    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def engine(app):
    engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'))

    _db.create_all()

    yield engine

    _db.close_all_sessions()
    engine.clear_compiled_cache()
    _db.drop_all()


@pytest.fixture(scope='module')
def connection(engine):
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    trans = connection.begin()
    sc_session = sessionmaker(bind=connection, expire_on_commit=False)

    yield sc_session

    trans.rollback()


@pytest.fixture(scope='function')
def client(app, engine):
    client = app.test_client()

    yield client


@pytest.fixture(scope='function')
def account_repository(session) -> AccountRepository:
    repository = AccountRepository(
        session=session,
    )

    yield repository


@pytest.fixture(scope='function')
def account_service(account_repository) -> AccountService:
    service = AccountService(
        account_repository=account_repository,
    )

    yield service


@pytest.fixture(scope='session')
def unique_account_iterator():
    def unique_account_generator():
        i = 1
        while True:
            yield {
                'name': f'name-{i}'
            }
            i += 1
    yield unique_account_generator()


@pytest.fixture(scope='function')
def unique_account(unique_account_iterator) -> dict:
    yield next(unique_account_iterator)


@pytest.fixture(scope='function')
def mall_repository(session) -> MallRepository:
    repository = MallRepository(
        session=session,
    )

    yield repository


@pytest.fixture(scope='function')
def mall_service(mall_repository) -> MallService:
    service = MallService(
        mall_repository=mall_repository,
    )

    yield service


@pytest.fixture(scope='session')
def unique_mall_iterator():
    def unique_mall_generator():
        i = 1
        while True:
            yield {
                'name': f'name-{i}'
            }
            i += 1
    yield unique_mall_generator()


@pytest.fixture(scope='function')
def unique_mall(unique_mall_iterator) -> dict:
    yield next(unique_mall_iterator)
    

@pytest.fixture(scope='function')
def unit_repository(session) -> UnitRepository:
    repository = UnitRepository(
        session=session,
    )

    yield repository


@pytest.fixture(scope='function')
def unit_service(unit_repository) -> UnitService:
    service = UnitService(
        unit_repository=unit_repository,
    )

    yield service


@pytest.fixture(scope='session')
def unique_unit_iterator():
    def unique_unit_generator():
        i = 1
        while True:
            yield {
                'name': f'name-{i}'
            }
            i += 1
    yield unique_unit_generator()


@pytest.fixture(scope='function')
def unique_unit(unique_unit_iterator) -> dict:
    yield next(unique_unit_iterator)