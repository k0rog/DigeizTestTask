import psycopg2.errors
from sqlalchemy.orm import sessionmaker, joinedload
from injector import inject

from api.models.unit import Unit

from werkzeug.exceptions import NotFound
from sqlalchemy.exc import IntegrityError
from api.exceptions import AlreadyExistsException, DoesNotExistException


class UnitRepository:
    @inject
    def __init__(
        self,
        session: sessionmaker,
    ):
        self._session = session

    def create(self, data: dict) -> Unit:
        unit = Unit(
            name=data['name'],
            mall_id=data['mall_id']
        )

        try:
            with self._session.begin() as session:
                session.add(unit)
        except IntegrityError as e:
            print(e)
            if isinstance(e.orig, psycopg2.errors.ForeignKeyViolation):
                raise DoesNotExistException('Mall does not exist!')
            elif isinstance(e.orig, psycopg2.errors.IntegrityError):
                raise AlreadyExistsException('Unit already exists!')

            raise e

        return unit

    def get_list(self, page: int, per_page: int) -> dict:
        Unit.query.with_session(self._session)
        try:
            with self._session.begin() as session:
                pagination_result = Unit.query.with_session(
                    session=session
                ).options(joinedload('mall')).order_by(Unit.id).paginate(
                    page=page,
                    per_page=per_page,
                    error_out=True,
                    max_per_page=50
                )
        except NotFound:
            raise DoesNotExistException('`page` or `per_page` specified incorrectly or units are not found!')

        return {
            'total': pagination_result.total,
            'units': pagination_result.items
        }

    def update(self, unit_id: int, data: dict) -> bool:
        try:
            with self._session.begin() as session:
                is_updated = session.query(
                    Unit
                ).filter_by(id=unit_id).update(data)
        except IntegrityError as e:
            if isinstance(e.orig, psycopg2.errors.IntegrityError):
                raise AlreadyExistsException('Unit already exists!')
            raise e

        return bool(is_updated)

    def delete(self, unit_id: int) -> bool:
        with self._session.begin() as session:
            is_deleted = session.query(
                Unit
            ).filter_by(id=unit_id).delete()

        return bool(is_deleted)

    def get(self, unit_id: int) -> Unit:
        with self._session.begin() as session:
            unit = session.query(
                Unit
            ).options(joinedload('mall')).get(unit_id)

        if not unit:
            raise DoesNotExistException('Unit does not exist!')

        return unit
