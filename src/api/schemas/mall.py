from marshmallow import fields, Schema, validate, validates, ValidationError

from api.schemas.unit import UnitRetrieveSchema


class BaseMallSchema(Schema):
    id = fields.Integer()
    name = fields.String(
        validate=validate.Length(max=255)
    )


class MallCreateSchema(BaseMallSchema):
    class Meta:
        dump_only = ('id',)
    account_id = fields.Integer(required=True)
    name = fields.String(
        validate=validate.Length(max=255),
        required=True
    )


class MallUpdateSchema(BaseMallSchema):
    class Meta:
        dump_only = ('id',)


class MallRetrieveSchema(BaseMallSchema):
    class Meta:
        dump_only = ('all',)
    units = fields.Nested(UnitRetrieveSchema(), many=True)
    account_id = fields.Integer()


class MallListSchema(Schema):
    class Meta:
        load_only = ('page', 'per_page')
        dump_only = ('malls', 'total')

    page = fields.Integer()
    per_page = fields.Integer(
        validate=validate.Range(1, 50)
    )

    total = fields.Integer()
    malls = fields.Nested(MallRetrieveSchema(), many=True, exclude=('units',))

    @validates('page')
    def validate_page(self, value):
        if value < 1:
            raise ValidationError('Wrong page value! Try value > 1.')
        return value
