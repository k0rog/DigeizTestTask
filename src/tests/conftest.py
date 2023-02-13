import pytest

from sqlalchemy.orm import sessionmaker
from testing.postgresql import Postgresql
from sqlalchemy import create_engine

from api.app import create_app
from api.models.account import Account
from api.models.mall import Mall

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

    config_class = get_config_class('../.env.test')
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


@pytest.fixture(scope='module')
def permanent_session(connection):
    sc_session = sessionmaker(bind=connection, expire_on_commit=False)

    yield sc_session


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


@pytest.fixture(scope='function')
def account_data():
    yield {
        'name': 'account_name'
    }


@pytest.fixture(scope='function')
def account(session, account_data):
    with session.begin() as session:
        account = Account(**account_data)
        session.add(account)

    yield account


@pytest.fixture(scope='function')
def mall_data(account):
    yield {
        'name': 'mall_name',
        'account_id': account.id
    }


@pytest.fixture(scope='function')
def mall(session, mall_data):
    with session.begin() as session:
        mall = Mall(**mall_data)
        session.add(mall)

    yield mall


@pytest.fixture(scope='function')
def unit_data(mall):
    yield {
        'name': 'unit_name',
        'mall_id': mall.id
    }


@pytest.fixture(scope='session')
def permanent_account_data_iterator():
    def permanent_account_data_generator():
        i = 1
        while True:
            yield {
                'name': f'name-{i}'
            }
            i += 1
    yield permanent_account_data_generator()


@pytest.fixture(scope='function')
def permanent_account_data(permanent_account_data_iterator):
    yield next(permanent_account_data_iterator)


@pytest.fixture(scope='function')
def permanent_account(permanent_session, permanent_account_data):
    with permanent_session.begin() as session:
        account = Account(**permanent_account_data)
        session.add(account)

    yield account


@pytest.fixture(scope='session')
def permanent_mall_data_iterator():
    def permanent_mall_data_generator():
        i = 1
        while True:
            yield {
                'name': f'name-{i}'
            }
            i += 1
    yield permanent_mall_data_generator()


@pytest.fixture(scope='function')
def permanent_mall_data(permanent_mall_data_iterator, permanent_account):
    data = next(permanent_mall_data_iterator)
    data['account_id'] = permanent_account.id
    yield data


@pytest.fixture(scope='function')
def permanent_mall(permanent_session, permanent_mall_data):
    with permanent_session.begin() as session:
        mall = Mall(**permanent_mall_data)
        session.add(mall)

    yield mall


@pytest.fixture(scope='session')
def permanent_unit_data_iterator():
    def permanent_unit_data_generator():
        i = 1
        while True:
            yield {
                'name': f'name-{i}'
            }
            i += 1
    yield permanent_unit_data_generator()


@pytest.fixture(scope='function')
def permanent_unit_data(permanent_unit_data_iterator, permanent_mall):
    data = next(permanent_unit_data_iterator)
    data['mall_id'] = permanent_mall.id
    yield data
