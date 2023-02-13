from marshmallow import fields, Schema, validate

from api.schemas.unit import UnitRetrieveSchema
from api.schemas.base import BasePaginationSchema


class MallCreateSchema(Schema):
    class Meta:
        dump_only = ('id',)

    id = fields.Integer()
    account_id = fields.Integer(required=True)
    name = fields.String(
        validate=validate.Length(max=255),
        required=True
    )


class MallUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(max=255))


class MallRetrieveSchema(Schema):
    id = fields.Integer()
    name = fields.String(validate=validate.Length(max=255))
    units = fields.Nested(UnitRetrieveSchema(), many=True)
    account_id = fields.Integer()


class MallListSchema(BasePaginationSchema):
    class Meta:
        dump_only = ('malls', 'total')

    malls = fields.Nested(MallRetrieveSchema(), many=True, exclude=('units',))


class MallBulkCreateSchema(Schema):
    malls = fields.List(fields.Nested(MallCreateSchema()))
