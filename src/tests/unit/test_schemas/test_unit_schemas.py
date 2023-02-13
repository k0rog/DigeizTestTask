import json
import marshmallow.exceptions
import pytest

from api.schemas.unit import (
    UnitCreateSchema,
    UnitListSchema,
    UnitUpdateSchema,
    UnitRetrieveSchema,
    UnitBulkCreateSchema
)


UNIT_DATA = {
    'name': 'unit_name',
    'mall_id': 1
}


class TestUnitCreateSchema:
    schema_class = UnitCreateSchema

    def test_with_valid_data(self):
        schema = self.schema_class()

        data = schema.loads(json.dumps(UNIT_DATA))

        assert data['name'] == UNIT_DATA['name']
        assert data['mall_id'] == UNIT_DATA['mall_id']

    @pytest.mark.parametrize(
        'field,value',
        (
                ('id', 1),
        )
    )
    def test_for_not_loaded_fields(self, field, value):
        schema = self.schema_class()

        create_data = UNIT_DATA.copy()
        create_data[field] = value

        with pytest.raises(marshmallow.exceptions.ValidationError):
            schema.loads(json.dumps(create_data))

    def test_id_is_dumped(self):
        schema = self.schema_class()

        validated_data = UNIT_DATA.copy()
        validated_data['id'] = 1

        return_data = schema.dump(validated_data)

        assert 'id' in return_data

    @pytest.mark.parametrize(
        'field, value',
        (
                ('name', 1),
                ('mall_id', 'str')
        )
    )
    def test_with_wrong_type(self, field, value):
        wrong_data = UNIT_DATA.copy()
        wrong_data[field] = value

        schema = self.schema_class()

        with pytest.raises(marshmallow.exceptions.ValidationError) as exception_info:
            schema.loads(json.dumps(wrong_data))

        error_message_dict = exception_info.value.messages
        assert len(error_message_dict) == 1
        assert field in error_message_dict

    def test_with_invalid_name(self):
        wrong_data = UNIT_DATA.copy()
        wrong_data['name'] = ''.join(['_' for _ in range(257)])

        schema = self.schema_class()

        with pytest.raises(marshmallow.exceptions.ValidationError) as exception_info:
            schema.loads(json.dumps(wrong_data))

        error_message_dict = exception_info.value.messages
        assert len(error_message_dict) == 1
        assert 'name' in error_message_dict
        assert error_message_dict['name'][0] == f'Longer than maximum length 255.'


class TestUnitUpdateSchema:
    schema_class = UnitUpdateSchema

    def test_with_valid_data(self):
        schema = self.schema_class(partial=True)

        data = schema.loads(json.dumps({'name': 'unit_name'}))

        assert data['name'] == UNIT_DATA['name']

    def test_partial(self):
        schema = self.schema_class(partial=True)

        data = {}
        schema.loads(json.dumps(data))

    @pytest.mark.parametrize(
        'field, value',
        (
                ('name', 1),
                ('mall_id', 'str')
        )
    )
    def test_with_wrong_type(self, field, value):
        wrong_data = UNIT_DATA.copy()
        del wrong_data['mall_id']
        wrong_data[field] = value

        schema = UnitUpdateSchema()

        with pytest.raises(marshmallow.exceptions.ValidationError) as exception_info:
            schema.loads(json.dumps(wrong_data))

        error_message_dict = exception_info.value.messages
        assert len(error_message_dict) == 1
        assert field in error_message_dict


class TestUnitRetrieveSchema:
    def test_dump_schema(self):
        schema = UnitRetrieveSchema()

        unit_data = UNIT_DATA.copy()
        unit_data.update({
            'id': 1,
        })

        retrieve_data = json.loads(schema.dumps(unit_data))

        assert 'id' in retrieve_data
        assert 'name' in retrieve_data
        assert 'mall_id' in retrieve_data


class TestUnitListSchema:
    schema_class = UnitListSchema

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
    schema_class = UnitBulkCreateSchema

    def test_load(self):
        data = {
            'units': [
                {
                    'name': 'first_unit_name',
                    'mall_id': 1
                }, {
                    'name': 'last_unit_name',
                    'mall_id': 2
                }
            ]
        }

        schema = self.schema_class()

        schema.loads(json.dumps(data))
