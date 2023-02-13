from marshmallow import fields, Schema, validate

from api.schemas.base import BasePaginationSchema
from api.schemas.mall import MallRetrieveSchema


class AccountCreateSchema(Schema):
    class Meta:
        dump_only = ('id',)

    id = fields.Integer()
    name = fields.String(
        validate=validate.Length(max=255),
        required=True
    )


class AccountUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(max=255))


class AccountRetrieveSchema(Schema):
    id = fields.Integer()
    name = fields.String(validate=validate.Length(max=255))
    malls = fields.Nested(MallRetrieveSchema(), exclude=('units',), many=True)


class AccountListSchema(BasePaginationSchema):
    class Meta:
        dump_only = ('accounts', 'total')

    accounts = fields.Nested(AccountRetrieveSchema(), many=True, exclude=('malls',))


class AccountBulkCreateSchema(Schema):
    accounts = fields.List(fields.Nested(AccountCreateSchema()))
