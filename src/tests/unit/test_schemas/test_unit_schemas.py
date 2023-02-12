import json
import marshmallow.exceptions
import pytest

from api.schemas.unit import (
    UnitCreateSchema,
    UnitListSchema,
    UnitUpdateSchema,
    UnitRetrieveSchema,
)


ACCOUNT_ID = 1
ACCOUNT_NAME = 'unit_name'


ACCOUNT_DATA = {
    'name': 'unit_name',
}


class TestUnitCreateSchema:
    def test_with_valid_data(self):
        schema = UnitCreateSchema()

        data = schema.loads(json.dumps(ACCOUNT_DATA))

        assert data['name'] == ACCOUNT_DATA['name']

    @pytest.mark.parametrize(
        'field,value',
        (
                ('id', 1),
        )
    )
    def test_field_is_not_loaded(self, field, value):
        schema = UnitCreateSchema()

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
        schema = UnitCreateSchema()

        validated_data = ACCOUNT_DATA.copy()
        validated_data[field] = value

        return_data = schema.dump(validated_data)

        assert field in return_data

    @pytest.mark.parametrize('field', ('name',))
    @pytest.mark.parametrize('value', (1,))
    def test_with_wrong_type(self, field, value):
        wrong_data = ACCOUNT_DATA.copy()
        wrong_data[field] = value

        schema = UnitCreateSchema()

        with pytest.raises(marshmallow.exceptions.ValidationError) as exception_info:
            schema.loads(json.dumps(wrong_data))

        error_message_dict = exception_info.value.messages
        assert len(error_message_dict) == 1
        assert field in error_message_dict
        assert error_message_dict[field][0] == f'Not a valid string.'


class TestUnitUpdateSchema:
    def test_with_valid_data(self):
        schema = UnitUpdateSchema()

        data = schema.loads(json.dumps(ACCOUNT_DATA))

        assert data['name'] == ACCOUNT_DATA['name']

    @pytest.mark.parametrize(
        'field,value',
        (
                ('id', 1),
        )
    )
    def test_field_is_not_loaded(self, field, value):
        schema = UnitCreateSchema()

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
        schema = UnitCreateSchema()

        validated_data = ACCOUNT_DATA.copy()
        validated_data[field] = value

        return_data = schema.dump(validated_data)

        assert field in return_data

    @pytest.mark.parametrize('field', ('name',))
    @pytest.mark.parametrize('value', (1,))
    def test_with_wrong_type(self, field, value):
        wrong_data = ACCOUNT_DATA.copy()
        wrong_data[field] = value

        schema = UnitUpdateSchema()

        with pytest.raises(marshmallow.exceptions.ValidationError) as exception_info:
            schema.loads(json.dumps(wrong_data))

        error_message_dict = exception_info.value.messages
        assert len(error_message_dict) == 1
        assert field in error_message_dict
        assert error_message_dict[field][0] == f'Not a valid string.'


class TestUnitRetrieveSchema:
    def test_dump_schema(self):
        schema = UnitRetrieveSchema()

        unit_data = ACCOUNT_DATA.copy()
        unit_data['id'] = 1

        retrieve_data = schema.dumps(unit_data)

        assert 'id' in retrieve_data
        assert 'name' in retrieve_data


class TestUnitListSchema:
    def test_valid_load(self):
        schema = UnitListSchema()

        schema.loads(json.dumps({
            'page': 1,
            'per_page': 10
        }))

    def test_with_negative_page(self):
        schema = UnitListSchema()
        data = {
            'page': -1,
            'per_page': 10
        }

        with pytest.raises(marshmallow.exceptions.ValidationError):
            schema.loads(json.dumps(data))

    def test_with_negative_per_page(self):
        schema = UnitListSchema()
        data = {
            'page': 1,
            'per_page': -1
        }

        with pytest.raises(marshmallow.exceptions.ValidationError):
            schema.loads(json.dumps(data))

    def test_with_too_big_per_page(self):
        schema = UnitListSchema()
        data = {
            'page': 1,
            'per_page': 100
        }

        with pytest.raises(marshmallow.exceptions.ValidationError):
            schema.loads(json.dumps(data))

    def test_valid_dump(self):
        schema = UnitListSchema()
        data = {
            'total': 100,
            'units': [{
                'id': i,
                'name': f'Unit-{i}'
            } for i in range(5)],
        }

        schema.dumps(data)
