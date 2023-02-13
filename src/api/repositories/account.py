import psycopg2.errors
from sqlalchemy.orm import sessionmaker, joinedload
from injector import inject

from api.models.account import Account

from werkzeug.exceptions import NotFound
from sqlalchemy.exc import IntegrityError
from api.exceptions import AlreadyExistsException, DoesNotExistException


class AccountRepository:
    @inject
    def __init__(
        self,
        session: sessionmaker,
    ):
        self._session = session

    def create(self, data: dict) -> Account:
        account = Account(
            name=data['name'],
        )

        try:
            with self._session.begin() as session:
                session.add(account)
        except IntegrityError:
            raise AlreadyExistsException('Account already exists!')

        return account

    def bulk_create(self, data: dict) -> None:
        try:
            with self._session.begin() as session:
                session.bulk_insert_mappings(
                    Account, [
                        account for account in data['accounts']
                    ]
                )
        except IntegrityError as e:
            if isinstance(e.orig, psycopg2.errors.UniqueViolation):
                raise AlreadyExistsException('One or more accounts already exist!')

            raise e

    def get_list(self, page: int, per_page: int) -> dict:
        Account.query.with_session(self._session)
        try:
            with self._session.begin() as session:
                pagination_result = Account.query.with_session(session=session).order_by(Account.id).paginate(
                    page=page,
                    per_page=per_page,
                    error_out=True,
                    max_per_page=50
                )
        except NotFound:
            raise DoesNotExistException('`page` or `per_page` specified incorrectly or accounts are not found!')

        return {
            'total': pagination_result.total,
            'accounts': pagination_result.items
        }

    def update(self, account_id: int, data: dict) -> bool:
        try:
            with self._session.begin() as session:
                is_updated = session.query(
                    Account
                ).filter_by(id=account_id).update(data)
        except IntegrityError:
            raise AlreadyExistsException('Account already exists!')

        return bool(is_updated)

    def delete(self, account_id: int) -> bool:
        with self._session.begin() as session:
            is_deleted = session.query(
                Account
            ).filter_by(id=account_id).delete()

        return bool(is_deleted)

    def get(self, account_id: int) -> Account:
        with self._session.begin() as session:
            account = session.query(
                Account
            ).options(joinedload('malls')).get(account_id)

        if not account:
            raise DoesNotExistException('Account does not exist!')

        return account
