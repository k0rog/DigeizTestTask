import psycopg2.errors
from sqlalchemy.orm import sessionmaker, joinedload
from injector import inject

from api.models.mall import Mall

from werkzeug.exceptions import NotFound
from sqlalchemy.exc import IntegrityError
from api.exceptions import AlreadyExistsException, DoesNotExistException


class MallRepository:
    @inject
    def __init__(
        self,
        session: sessionmaker,
    ):
        self._session = session

    def create(self, data: dict) -> Mall:
        mall = Mall(
            name=data['name'],
            account_id=data['account_id']
        )

        try:
            with self._session.begin() as session:
                session.add(mall)
        except IntegrityError as e:
            if isinstance(e.orig, psycopg2.errors.ForeignKeyViolation):
                raise DoesNotExistException('Account does not exist!')
            elif isinstance(e.orig, psycopg2.errors.IntegrityError):
                raise AlreadyExistsException('Mall already exists!')

            raise e
        return mall

    def bulk_create(self, data: dict) -> None:
        try:
            with self._session.begin() as session:
                session.bulk_insert_mappings(
                    Mall, [
                        mall for mall in data['malls']
                    ]
                )
        except IntegrityError as e:
            if isinstance(e.orig, psycopg2.errors.UniqueViolation):
                raise AlreadyExistsException('One or more malls already exist!')

            raise e

    def get_list(self, page: int, per_page: int) -> dict:
        Mall.query.with_session(self._session)
        try:
            with self._session.begin() as session:
                pagination_result = Mall.query.with_session(
                    session=session
                ).options(joinedload('account')).order_by(Mall.id).paginate(
                    page=page,
                    per_page=per_page,
                    error_out=True,
                    max_per_page=50
                )
        except NotFound:
            raise DoesNotExistException('`page` or `per_page` specified incorrectly or malls are not found!')

        return {
            'total': pagination_result.total,
            'malls': pagination_result.items
        }

    def update(self, mall_id: int, data: dict) -> bool:
        try:
            with self._session.begin() as session:
                is_updated = session.query(
                    Mall
                ).filter_by(id=mall_id).update(data)
        except IntegrityError as e:
            if isinstance(e.orig, psycopg2.errors.IntegrityError):
                raise AlreadyExistsException('Mall already exists!')
            raise e

        return bool(is_updated)

    def delete(self, mall_id: int) -> bool:
        with self._session.begin() as session:
            is_deleted = session.query(
                Mall
            ).filter_by(id=mall_id).delete()

        return bool(is_deleted)

    def get(self, mall_id: int) -> Mall:
        with self._session.begin() as session:
            mall = session.query(
                Mall
            ).options(joinedload('units')).get(mall_id)

        if not mall:
            raise DoesNotExistException('Mall does not exist!')

        return mall
