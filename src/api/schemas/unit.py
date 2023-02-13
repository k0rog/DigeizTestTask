from marshmallow import fields, Schema, validate

from api.schemas.base import BasePaginationSchema


class UnitCreateSchema(Schema):
    class Meta:
        dump_only = ('id',)

    id = fields.Integer()
    mall_id = fields.Integer(required=True)
    name = fields.String(
        validate=validate.Length(max=255),
        required=True
    )


class UnitUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(max=255))


class UnitRetrieveSchema(Schema):
    id = fields.Integer()
    name = fields.String(validate=validate.Length(max=255))
    mall_id = fields.Integer()


class UnitListSchema(BasePaginationSchema):
    class Meta:
        dump_only = ('units', 'total')

    units = fields.Nested(UnitRetrieveSchema(), many=True)


class UnitBulkCreateSchema(Schema):
    units = fields.List(fields.Nested(UnitCreateSchema()))
