import json
from http import HTTPStatus

from flask import request

from injector import inject
from flask_restful import Resource
from webargs.flaskparser import use_args

from api.services.account import AccountService
from api.utils.response_serializer import serialize_response
from api.schemas.account import (
    AccountCreateSchema,
    AccountUpdateSchema,
    AccountRetrieveSchema,
    AccountListSchema,
    AccountBulkCreateSchema
)


class AccountsBulkResource(Resource):
    @inject
    def __init__(self, service: AccountService):
        self.account_service = service

    @use_args(AccountBulkCreateSchema())
    @serialize_response(None, HTTPStatus.NO_CONTENT)
    def post(self, accounts):
        return self.account_service.bulk_create(accounts)


class AccountsResource(Resource):
    @inject
    def __init__(self, service: AccountService):
        self.account_service = service

    @use_args(AccountCreateSchema())
    @serialize_response(AccountCreateSchema(), HTTPStatus.CREATED)
    def post(self, account):
        return self.account_service.create(account)

    @use_args(AccountListSchema(), location='querystring', as_kwargs=True)
    @serialize_response(AccountListSchema(), HTTPStatus.OK)
    def get(self, page=1, per_page=20):
        return self.account_service.get_list(page, per_page)


class AccountResource(Resource):
    @inject
    def __init__(self, repository: AccountService):
        self.account_service = repository

    @use_args(AccountUpdateSchema())
    @serialize_response(None, HTTPStatus.NO_CONTENT)
    def patch(self, account: dict, account_id: int):
        self.account_service.update(account_id, account)

    @serialize_response(None, HTTPStatus.NO_CONTENT)
    def delete(self, account_id: int):
        self.account_service.delete(account_id)

    @serialize_response(AccountRetrieveSchema(), HTTPStatus.OK)
    def get(self, account_id: int):
        return self.account_service.get(account_id)
