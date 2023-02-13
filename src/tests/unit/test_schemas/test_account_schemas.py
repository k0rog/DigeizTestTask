import json
import marshmallow.exceptions
import pytest

from api.schemas.account import (
    AccountCreateSchema,
    AccountListSchema,
    AccountUpdateSchema,
    AccountRetrieveSchema,
    AccountBulkCreateSchema
)

ACCOUNT_DATA = {
    'name': 'account_name',
}


class TestAccountCreateSchema:
    schema_class = AccountCreateSchema

    def test_with_valid_data(self):
        schema = self.schema_class()

        data = schema.loads(json.dumps(ACCOUNT_DATA))

        assert data['name'] == ACCOUNT_DATA['name']

    @pytest.mark.parametrize(
        'field,value',
        (
                ('id', 1),
        )
    )
    def test_for_not_loaded_fields(self, field, value):
        schema = self.schema_class()

        create_data = ACCOUNT_DATA.copy()
        create_data[field] = value

        with pytest.raises(marshmallow.exceptions.ValidationError):
            schema.loads(json.dumps(create_data))

    def test_id_is_dumped(self):
        schema = self.schema_class()

        validated_data = ACCOUNT_DATA.copy()
        validated_data['id'] = 1

        return_data = schema.dump(validated_data)

        assert 'id' in return_data

    @pytest.mark.parametrize(
        'field,value',
        (
                ('name', 1),
        )
    )
    def test_with_wrong_type(self, field, value):
        wrong_data = ACCOUNT_DATA.copy()
        wrong_data[field] = value

        schema = self.schema_class()

        with pytest.raises(marshmallow.exceptions.ValidationError) as exception_info:
            schema.loads(json.dumps(wrong_data))

        error_message_dict = exception_info.value.messages
        assert len(error_message_dict) == 1
        assert field in error_message_dict

    def test_with_invalid_name(self):
        wrong_data = ACCOUNT_DATA.copy()
        wrong_data['name'] = ''.join(['_' for _ in range(257)])

        schema = self.schema_class()

        with pytest.raises(marshmallow.exceptions.ValidationError) as exception_info:
            schema.loads(json.dumps(wrong_data))

        error_message_dict = exception_info.value.messages
        assert len(error_message_dict) == 1
        assert 'name' in error_message_dict
        assert error_message_dict['name'][0] == f'Longer than maximum length 255.'


class TestAccountUpdateSchema:
    schema_class = AccountUpdateSchema

    def test_with_valid_data(self):
        schema = self.schema_class(partial=True)

        data = schema.loads(json.dumps(ACCOUNT_DATA))

        assert data['name'] == ACCOUNT_DATA['name']

    def test_partial(self):
        schema = self.schema_class(partial=True)

        data = {}
        schema.loads(json.dumps(data))

    @pytest.mark.parametrize(
        'field,value',
        (
                ('name', 1),
        )
    )
    def test_with_wrong_type(self, field, value):
        wrong_data = ACCOUNT_DATA.copy()
        wrong_data[field] = value

        schema = AccountUpdateSchema()

        with pytest.raises(marshmallow.exceptions.ValidationError) as exception_info:
            schema.loads(json.dumps(wrong_data))

        error_message_dict = exception_info.value.messages
        assert len(error_message_dict) == 1
        assert field in error_message_dict


class TestAccountRetrieveSchema:
    def test_dump_schema(self):
        schema = AccountRetrieveSchema()

        account_data = ACCOUNT_DATA.copy()
        account_data.update({
            'id': 1,
            'malls': [{
                'id': 1,
                'name': 'mall_name'
            }, {
                'id': 2,
                'name': 'second_name'
            }
            ]
        })

        retrieve_data = json.loads(schema.dumps(account_data))

        assert 'id' in retrieve_data
        assert 'name' in retrieve_data
        assert 'malls' in retrieve_data
        assert 'id' in retrieve_data['malls'][0] and 'name' in retrieve_data['malls'][0]


class TestAccountListSchema:
    schema_class = AccountListSchema

    def test_valid_load(self):
        schema = self.schema_class()

        schema.loads(json.dumps({
            'page': 1,
            'per_page': 10
        }))

    def test_with_negative_page(self):
        schema = self.schema_class()
        data = {
            'page': -1,
            'per_page': 10
        }

        with pytest.raises(marshmallow.exceptions.ValidationError):
            schema.loads(json.dumps(data))

    def test_with_negative_per_page(self):
        schema = self.schema_class()
        data = {
            'page': 1,
            'per_page': -1
        }

        with pytest.raises(marshmallow.exceptions.ValidationError):
            schema.loads(json.dumps(data))

    def test_with_too_big_per_page(self):
        schema = self.schema_class()
        data = {
            'page': 1,
            'per_page': 100
        }

        with pytest.raises(marshmallow.exceptions.ValidationError):
            schema.loads(json.dumps(data))

    def test_valid_dump(self):
        schema = self.schema_class()
        data = {
            'total': 100,
            'accounts': [{
                'id': i,
                'name': f'Account-{i}'
            } for i in range(5)],
        }

        schema.dumps(data)


class TestBulkCreateSchema:
    schema_class = AccountBulkCreateSchema

    def test_load(self):
        data = {
            'accounts': [
                {
                    'name': 'first_account_name'
                }, {
                    'name': 'last_account_name'
                }
            ]
        }

        schema = self.schema_class()

        schema.loads(json.dumps(data))
