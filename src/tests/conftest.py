from dotenv import load_dotenv

load_dotenv('../.env.test')


import pytest

from sqlalchemy.orm import sessionmaker
from testing.postgresql import Postgresql
from sqlalchemy import create_engine

from api.app import create_app
from api.repositories.account import AccountRepository
from api.services.account import AccountService
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

    config_class = get_config_class()
    config_class.SQLALCHEMY_DATABASE_URI = sqlalchemy_database_url

    app = create_app(config_class)

    app.config.update({
        'TESTING': True,
    })

    with app.app_context():
        yield app


@pytest.fixture(scope='session')
def engine(app):
    engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'))

    _db.create_all()

    yield engine

    _db.close_all_sessions()
    engine.clear_compiled_cache()
    _db.drop_all()


@pytest.fixture(scope='session')
def connection(engine):
    connection = engine.connect()
    yield connection
    connection.close()


# @pytest.fixture(scope='function')
# async def session(connection):
#     trans = await connection.begin()
#     session = scoped_session(
#         sessionmaker(
#             connection, class_=AsyncSession, expire_on_commit=False
#         )
#     )
#
#     yield session
#     await trans.rollback()

@pytest.fixture(scope='function')
def session(connection):
    trans = connection.begin()
    sc_session = sessionmaker(bind=connection, expire_on_commit=False)

    yield sc_session

    trans.rollback()


# @pytest.fixture(scope='function')
# def client(app, storage):
#     client = app.test_client()
#
#     yield client
#
#
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
#
#
# @pytest.fixture(scope='function')
# def bank_card_repository(storage) -> BankCardRepository:
#     repository = BankCardRepository(
#         storage=storage,
#     )
#
#     yield repository
#
#
# @pytest.fixture(scope='session')
# def permanent_session(db):
#     session = db.session
#     yield session
#     session.close()
#
#
# @pytest.fixture(scope='session')
# def bank_account(permanent_session):
#     while True:
#         try:
#             bank_account = BankAccount(
#                 currency='BYN',
#                 balance=0,
#             )
#
#             permanent_session.add(bank_account)
#             permanent_session.commit()
#
#             break
#         except IntegrityError:
#             '''There's very small chance to generate duplicated IBAN
#             But since this chance still exists, we have to repeat the operation'''
#             permanent_session.rollback()
#         except SQLAlchemyError:
#             permanent_session.rollback()
#             raise
#
#     association_row = AssociationBankAccountCustomer(
#         bank_account_id=bank_account.IBAN,
#         customer_id='MockUUID'
#     )
#
#     permanent_session.add(association_row)
#     permanent_session.commit()
#
#     yield bank_account
#
#
# @pytest.fixture(scope='session')
# def customer(permanent_session):
#     customer = Customer(
#         first_name='John',
#         last_name='Smith',
#         email='jsmith@gmail.com',
#         passport_number='HB2222222',
#     )
#
#     permanent_session.add(customer)
#
#     try:
#         permanent_session.commit()
#     except SQLAlchemyError:
#         permanent_session.rollback()
#         raise
#
#     yield customer
