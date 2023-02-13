import json
import marshmallow.exceptions
import pytest

from api.schemas.mall import (
    MallCreateSchema,
    MallListSchema,
    MallUpdateSchema,
    MallRetrieveSchema,
    MallBulkCreateSchema
)


MALL_DATA = {
    'name': 'mall_name',
    'account_id': 1
}


class TestMallCreateSchema:
    schema_class = MallCreateSchema

    def test_with_valid_data(self):
        schema = self.schema_class()

        data = schema.loads(json.dumps(MALL_DATA))

        assert data['name'] == MALL_DATA['name']
        assert data['account_id'] == MALL_DATA['account_id']

    @pytest.mark.parametrize(
        'field,value',
        (
                ('id', 1),
        )
    )
    def test_for_not_loaded_fields(self, field, value):
        schema = self.schema_class()

        create_data = MALL_DATA.copy()
        create_data[field] = value

        with pytest.raises(marshmallow.exceptions.ValidationError):
            schema.loads(json.dumps(create_data))

    def test_id_is_dumped(self):
        schema = self.schema_class()

        validated_data = MALL_DATA.copy()
        validated_data['id'] = 1

        return_data = schema.dump(validated_data)

        assert 'id' in return_data

    @pytest.mark.parametrize(
        'field, value',
        (
                ('name', 1),
                ('account_id', 'str')
        )
    )
    def test_with_wrong_type(self, field, value):
        wrong_data = MALL_DATA.copy()
        wrong_data[field] = value

        schema = self.schema_class()

        with pytest.raises(marshmallow.exceptions.ValidationError) as exception_info:
            schema.loads(json.dumps(wrong_data))

        error_message_dict = exception_info.value.messages
        assert len(error_message_dict) == 1
        assert field in error_message_dict

    def test_with_invalid_name(self):
        wrong_data = MALL_DATA.copy()
        wrong_data['name'] = ''.join(['_' for _ in range(257)])

        schema = self.schema_class()

        with pytest.raises(marshmallow.exceptions.ValidationError) as exception_info:
            schema.loads(json.dumps(wrong_data))

        error_message_dict = exception_info.value.messages
        assert len(error_message_dict) == 1
        assert 'name' in error_message_dict
        assert error_message_dict['name'][0] == f'Longer than maximum length 255.'


class TestMallUpdateSchema:
    schema_class = MallUpdateSchema

    def test_with_valid_data(self):
        schema = self.schema_class(partial=True)

        data = schema.loads(json.dumps({'name': 'mall_name'}))

        assert data['name'] == MALL_DATA['name']

    def test_partial(self):
        schema = self.schema_class(partial=True)

        data = {}
        schema.loads(json.dumps(data))

    @pytest.mark.parametrize(
        'field, value',
        (
                ('name', 1),
                ('account_id', 'str')
        )
    )
    def test_with_wrong_type(self, field, value):
        wrong_data = MALL_DATA.copy()
        del wrong_data['account_id']
        wrong_data[field] = value

        schema = MallUpdateSchema()

        with pytest.raises(marshmallow.exceptions.ValidationError) as exception_info:
            schema.loads(json.dumps(wrong_data))

        error_message_dict = exception_info.value.messages
        assert len(error_message_dict) == 1
        assert field in error_message_dict


class TestMallRetrieveSchema:
    def test_dump_schema(self):
        schema = MallRetrieveSchema()

        mall_data = MALL_DATA.copy()
        mall_data.update({
            'id': 1,
            'units': [{
                'id': 1,
                'name': 'unit_name'
            }, {
                'id': 2,
                'name': 'unit_second_name'
            }
            ]
        })

        retrieve_data = json.loads(schema.dumps(mall_data))

        assert 'id' in retrieve_data
        assert 'name' in retrieve_data
        assert 'units' in retrieve_data
        assert 'account_id' in retrieve_data
        assert 'id' in retrieve_data['units'][0] and 'name' in retrieve_data['units'][0]


class TestMallListSchema:
    schema_class = MallListSchema

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
            'units': [{
                'id': i,
                'name': f'Unit-{i}'
            } for i in range(5)],
        }

        schema.dumps(data)


class TestBulkCreateSchema:
    schema_class = MallBulkCreateSchema

    def test_load(self):
        data = {
            'malls': [
                {
                    'name': 'first_mall_name',
                    'account_id': 1
                }, {
                    'name': 'last_mall_name',
                    'account_id': 2
                }
            ]
        }

        schema = self.schema_class()

        schema.loads(json.dumps(data))
