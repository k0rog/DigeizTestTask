from http import HTTPStatus

from injector import inject
from flask_restful import Resource
from webargs.flaskparser import use_args

from api.services.unit import UnitService
from api.utils.response_serializer import serialize_response
from api.schemas.unit import UnitCreateSchema, UnitUpdateSchema, UnitRetrieveSchema, UnitListSchema


class UnitsResource(Resource):
    @inject
    def __init__(self, service: UnitService):
        self.unit_service = service

    @use_args(UnitCreateSchema())
    @serialize_response(UnitCreateSchema(), HTTPStatus.CREATED)
    def post(self, unit):
        return self.unit_service.create(unit)

    @use_args(UnitListSchema(), location='querystring', as_kwargs=True)
    @serialize_response(UnitListSchema(), HTTPStatus.OK)
    def get(self, page=1, per_page=20):
        return self.unit_service.get_list(page, per_page)


class UnitResource(Resource):
    @inject
    def __init__(self, repository: UnitService):
        self.unit_service = repository

    @use_args(UnitUpdateSchema())
    @serialize_response(None, HTTPStatus.NO_CONTENT)
    def patch(self, unit: dict, unit_id: int):
        self.unit_service.update(unit_id, unit)

    @serialize_response(None, HTTPStatus.NO_CONTENT)
    def delete(self, unit_id: int):
        self.unit_service.delete(unit_id)

    @serialize_response(UnitRetrieveSchema(), HTTPStatus.OK)
    def get(self, unit_id: int):
        return self.unit_service.get(unit_id)
