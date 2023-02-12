from marshmallow import fields, Schema, validate, validates, ValidationError


class BaseUnitSchema(Schema):
    id = fields.Integer()
    name = fields.String(
        validate=validate.Length(max=255),
    )


class UnitCreateSchema(BaseUnitSchema):
    class Meta:
        dump_only = ('id',)
    mall_id = fields.Integer(required=True)
    name = fields.String(
        validate=validate.Length(max=255),
        required=True
    )


class UnitUpdateSchema(BaseUnitSchema):
    class Meta:
        dump_only = ('id',)


class UnitRetrieveSchema(BaseUnitSchema):
    class Meta:
        dump_only = ('all',)
    mall_id = fields.Integer()


class UnitListSchema(Schema):
    class Meta:
        load_only = ('page', 'per_page')
        dump_only = ('units', 'total')

    page = fields.Integer()
    per_page = fields.Integer(
        validate=validate.Range(1, 50)
    )

    total = fields.Integer()
    units = fields.Nested(UnitRetrieveSchema(), many=True)

    @validates('page')
    def validate_page(self, value):
        if value < 1:
            raise ValidationError('Wrong page value! Try value > 1.')
        return value
