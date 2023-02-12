from marshmallow import fields, Schema, validate, validates, ValidationError


class BaseAccountSchema(Schema):
    id = fields.Integer()
    name = fields.String(
        validate=validate.Length(max=255)
    )


class AccountCreateSchema(BaseAccountSchema):
    class Meta:
        dump_only = ('id',)


class AccountUpdateSchema(BaseAccountSchema):
    class Meta:
        dump_only = ('id',)


class AccountRetrieveSchema(BaseAccountSchema):
    class Meta:
        dump_only = ('all',)


class AccountListSchema(Schema):
    class Meta:
        load_only = ('page', 'per_page')
        dump_only = ('accounts', 'total')

    page = fields.Integer()
    per_page = fields.Integer(
        validate=validate.Range(1, 50)
    )

    total = fields.Integer()
    accounts = fields.Nested(AccountRetrieveSchema(), many=True)

    @validates('page')
    def validate_page(self, value):
        if value < 1:
            raise ValidationError('Wrong page value! Try value > 1.')
        return value
