import uuid
import json
import copy
import marshmallow.exceptions
import pytest

from api.schemas.account import (
    AccountCreateSchema,
    AccountListSchema,
    AccountUpdateSchema,
    AccountRetrieveSchema,
)


ACCOUNT_ID = 1
ACCOUNT_NAME = 'account_name'


ACCOUNT_DATA = {
    'name': 'account_name',
}


class TestAccountCreateSchema:
    def test_with_valid_data(self):
        schema = AccountCreateSchema()

        data = schema.loads(json.dumps(ACCOUNT_DATA))

        assert data['name'] == ACCOUNT_DATA['name']

    @pytest.mark.parametrize(
        'field,value',
        (
                ('id', 1),
        )
    )
    def test_field_is_not_loaded(self, field, value):
        schema = AccountCreateSchema()

        create_data = ACCOUNT_DATA.copy()
        create_data[field] = value

        with pytest.raises(marshmallow.exceptions.ValidationError):
            schema.loads(json.dumps(create_data))

    @pytest.mark.parametrize(
        'field,value',
        (
                ('id', 1),
        )
    )
    def test_id_is_dumped(self, field, value):
        schema = AccountCreateSchema()

        validated_data = ACCOUNT_DATA.copy()
        validated_data[field] = value

        return_data = schema.dump(validated_data)

        assert field in return_data

    @pytest.mark.parametrize('field', ('name',))
    @pytest.mark.parametrize('value', (1,))
    def test_with_wrong_type(self, field, value):
        wrong_data = ACCOUNT_DATA.copy()
        wrong_data[field] = value

        schema = AccountCreateSchema()

        with pytest.raises(marshmallow.exceptions.ValidationError) as exception_info:
            schema.loads(json.dumps(wrong_data))

        error_message_dict = exception_info.value.messages
        assert len(error_message_dict) == 1
        assert field in error_message_dict
        assert error_message_dict[field][0] == f'Not a valid string.'


class TestAccountUpdateSchema:
    def test_with_valid_data(self):
        schema = AccountUpdateSchema()

        data = schema.loads(json.dumps(ACCOUNT_DATA))

        assert data['name'] == ACCOUNT_DATA['name']

    @pytest.mark.parametrize(
        'field,value',
        (
                ('id', 1),
        )
    )
    def test_field_is_not_loaded(self, field, value):
        schema = AccountCreateSchema()

        create_data = ACCOUNT_DATA.copy()
        create_data[field] = value

        with pytest.raises(marshmallow.exceptions.ValidationError):
            schema.loads(json.dumps(create_data))

    @pytest.mark.parametrize(
        'field,value',
        (
                ('id', 1),
        )
    )
    def test_field_is_dumped(self, field, value):
        schema = AccountCreateSchema()

        validated_data = ACCOUNT_DATA.copy()
        validated_data[field] = value

        return_data = schema.dump(validated_data)

        assert field in return_data

    @pytest.mark.parametrize('field', ('name',))
    @pytest.mark.parametrize('value', (1,))
    def test_with_wrong_type(self, field, value):
        wrong_data = ACCOUNT_DATA.copy()
        wrong_data[field] = value

        schema = AccountUpdateSchema()

        with pytest.raises(marshmallow.exceptions.ValidationError) as exception_info:
            schema.loads(json.dumps(wrong_data))

        error_message_dict = exception_info.value.messages
        assert len(error_message_dict) == 1
        assert field in error_message_dict
        assert error_message_dict[field][0] == f'Not a valid string.'


class TestAccountRetrieveSchema:
    def test_dump_schema(self):
        schema = AccountRetrieveSchema()

        customer_data = ACCOUNT_DATA.copy()
        customer_data['id'] = 1

        retrieve_data = schema.dumps(customer_data)

        assert 'id' in retrieve_data
        assert 'name' in retrieve_data


class TestAccountListSchema:
    def test_valid_load(self):
        schema = AccountListSchema()

        schema.loads(json.dumps({
            'page': 1,
            'per_page': 10
        }))

    @pytest.mark.parametrize(
        'field',
        (
                ('page',),
                ('per_page',),
        )
    )
    def test_load_with_negative_value(self, field):
        schema = AccountListSchema()

        valid_data = {
            'page': 1,
            'per_page': 10
        }
        valid_data.update({
            field: -1
        })

        with pytest.raises()
        schema.loads(json.dumps())
