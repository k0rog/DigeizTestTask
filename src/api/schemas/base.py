from marshmallow import fields, Schema, validate, validates, ValidationError


class BasePaginationSchema(Schema):
    class Meta:
        load_only = ('page', 'per_page')
        dump_only = ('total',)

    page = fields.Integer()
    per_page = fields.Integer(
        validate=validate.Range(1, 50)
    )

    @validates('page')
    def validate_page(self, value):
        if value < 1:
            raise ValidationError('Wrong page value! Try value > 1.')
        return value

    total = fields.Integer()
