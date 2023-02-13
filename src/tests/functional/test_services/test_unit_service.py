import pytest

from api.exceptions import AlreadyExistsException, DoesNotExistException
from api.models.unit import Unit


class TestCreate:
    def test_is_id_returned(self, unit_service, unit_data):
        unit = unit_service.create(unit_data)

        assert hasattr(unit, 'id')

    def test_create(self, unit_service, session, unit_data):
        unit = unit_service.create(unit_data)

        with session.begin() as session:
            storage_unit = session.query(
                Unit
            ).get(unit.id)

        assert storage_unit is not None
        assert storage_unit.name == unit_data['name']

    def test_for_duplicated_name(self, unit_service, unit_data):
        unit_service.create(unit_data)

        with pytest.raises(AlreadyExistsException) as exception_info:
            unit_service.create(unit_data)

        assert exception_info.value.message == 'Unit already exists!'


class TestUpdate:
    def test_for_one_field(self, unit_service, session, unit_data):
        unit = unit_service.create(unit_data)

        update_data = {
            'name': 'updated_name'
        }

        unit_service.update(unit.id, update_data)

        with session.begin() as session:
            storage_unit = session.query(
                Unit
            ).get(unit.id)

        assert storage_unit.name == update_data['name']

    def test_for_duplicated_name(self, unit_service, unit_data):
        unit_service.create(unit_data)

        second_unit_data = unit_data.copy()
        second_unit_data.update({'name': 'second_unit_name'})

        second_unit = unit_service.create(second_unit_data)

        update_data = {
            'name': unit_data['name']
        }

        with pytest.raises(AlreadyExistsException) as exception_info:
            unit_service.update(second_unit.id, update_data)

        assert exception_info.value.message == 'Unit already exists!'


class TestDelete:
    def test_delete(self, unit_service, session, unit_data):
        unit = unit_service.create(unit_data)

        is_deleted = unit_service.delete(unit.id)

        assert is_deleted

        with session.begin() as session:
            assert session.query(
                Unit
            ).get(unit.id) is None

    def test_for_nonexistent_unit(self, unit_service):
        is_deleted = unit_service.delete(1000)

        assert not is_deleted


class TestGet:
    def test_get(self, unit_service, session, unit_data):
        unit = unit_service.create(unit_data)

        retrieved_unit = unit_service.get(unit.id)

        with session.begin() as session:
            storage_unit = session.query(
                Unit
            ).get(unit.id)

        assert storage_unit.name == retrieved_unit.name

    def test_for_nonexistent_unit(self, unit_service):
        with pytest.raises(DoesNotExistException) as exception_info:
            unit_service.get(1000)

        assert exception_info.value.message == 'Unit does not exist!'


class TestGetList:
    @pytest.mark.parametrize(
        'count_to_create,page,per_page',
        (
                (10, 1, 5),
                (10, 2, 5),
                (10, 3, 3)
        )
    )
    def test_get_list(self, unit_service, unit_data, count_to_create, page, per_page):
        created_units = []

        for i in range(count_to_create):
            unit_data = unit_data.copy()
            unit_data.update({'name': f'{unit_data["name"]}{i}'})

            created_units.append(
                unit_service.create(unit_data)
            )

        retrieved_units = unit_service.get_list(page, per_page)

        assert count_to_create == retrieved_units['total']

        created_units_skip = (page - 1) * per_page
        for i, retrieved_unit in enumerate(retrieved_units['units']):
            assert retrieved_unit.id == created_units[i + created_units_skip].id
            assert retrieved_unit.name == created_units[i + created_units_skip].name


class TestBulkCreate:
    def test_bulk_create(self, unit_service, session, mall):
        data = {'units': [{
            'name': 'first_unit',
            'mall_id': mall.id
        }, {
            'name': 'second_unit',
            'mall_id': mall.id
        }]}

        unit_service.bulk_create(data)

        with session.begin() as session:
            assert session.query(
                Unit
            ).filter(
                Unit.name.in_(
                    [unit['name'] for unit in data['units']]
                )
            ).count() == len(data['units'])

    def test_bulk_create_with_duplicated_data(self, unit_service, mall):
        data = {'units': [{
            'name': 'first_unit',
            'mall_id': mall.id
        }, {
            'name': 'second_unit',
            'mall_id': mall.id
        }]}

        unit_service.bulk_create(data)

        with pytest.raises(AlreadyExistsException) as exception_info:
            unit_service.bulk_create(data)

        assert exception_info.value.message == 'One or more units already exist!'
