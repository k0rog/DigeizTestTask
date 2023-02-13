from http import HTTPStatus

from injector import inject
from flask_restful import Resource
from webargs.flaskparser import use_args

from api.services.mall import MallService
from api.utils.response_serializer import serialize_response
from api.schemas.mall import (
    MallCreateSchema,
    MallUpdateSchema,
    MallRetrieveSchema,
    MallListSchema,
    MallBulkCreateSchema
)


class MallsBulkResource(Resource):
    @inject
    def __init__(self, service: MallService):
        self.account_service = service

    @use_args(MallBulkCreateSchema())
    @serialize_response(None, HTTPStatus.CREATED)
    def post(self, malls):
        return self.account_service.bulk_create(malls)


class MallsResource(Resource):
    @inject
    def __init__(self, service: MallService):
        self.mall_service = service

    @use_args(MallCreateSchema())
    @serialize_response(MallCreateSchema(), HTTPStatus.CREATED)
    def post(self, mall):
        return self.mall_service.create(mall)

    @use_args(MallListSchema(), location='querystring', as_kwargs=True)
    @serialize_response(MallListSchema(), HTTPStatus.OK)
    def get(self, page=1, per_page=20):
        return self.mall_service.get_list(page, per_page)


class MallResource(Resource):
    @inject
    def __init__(self, repository: MallService):
        self.mall_service = repository

    @use_args(MallUpdateSchema())
    @serialize_response(None, HTTPStatus.NO_CONTENT)
    def patch(self, mall: dict, mall_id: int):
        self.mall_service.update(mall_id, mall)

    @serialize_response(None, HTTPStatus.NO_CONTENT)
    def delete(self, mall_id: int):
        self.mall_service.delete(mall_id)

    @serialize_response(MallRetrieveSchema(), HTTPStatus.OK)
    def get(self, mall_id: int):
        return self.mall_service.get(mall_id)
