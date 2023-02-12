import pytest

from api.exceptions import AlreadyExistsException, DoesNotExistException
from api.models.unit import Unit


ACCOUNT_DATA = {
    'name': 'my_first_unit',
}


class TestCreate:
    def test_is_id_returned(self, unit_service):
        unit = unit_service.create(ACCOUNT_DATA)

        assert hasattr(unit, 'id')

    def test_create(self, unit_service, session):
        unit = unit_service.create(ACCOUNT_DATA)

        with session.begin() as session:
            storage_unit = session.query(
                Unit
            ).get(unit.id)

        assert storage_unit is not None
        assert storage_unit.name == ACCOUNT_DATA['name']

    def test_for_duplicated_name(self, unit_service):
        unit_service.create(ACCOUNT_DATA)

        with pytest.raises(AlreadyExistsException) as exception_info:
            unit_service.create(ACCOUNT_DATA)

        assert exception_info.value.message == 'Unit already exists!'


class TestUpdate:
    def test_for_one_field(self, unit_service, session):
        unit = unit_service.create(ACCOUNT_DATA)

        update_data = {
            'name': 'updated_name'
        }

        unit_service.update(unit.id, update_data)

        with session.begin() as session:
            storage_unit = session.query(
                Unit
            ).get(unit.id)

        assert storage_unit.name == update_data['name']

    def test_for_duplicated_name(self, unit_service):
        unit_service.create(ACCOUNT_DATA)

        second_unit_data = ACCOUNT_DATA.copy()
        second_unit_data.update({'name': 'second_unit_name'})

        second_unit = unit_service.create(second_unit_data)

        update_data = {
            'name': ACCOUNT_DATA['name']
        }

        with pytest.raises(AlreadyExistsException) as exception_info:
            unit_service.update(second_unit.id, update_data)

        assert exception_info.value.message == 'Unit already exists!'


class TestDelete:
    def test_delete(self, unit_service, session):
        unit = unit_service.create(ACCOUNT_DATA)

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
    def test_get(self, unit_service, session):
        unit = unit_service.create(ACCOUNT_DATA)

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
    def test_get_list(self, unit_service, count_to_create, page, per_page):
        created_units = []

        for i in range(count_to_create):
            unit_data = ACCOUNT_DATA.copy()
            unit_data.update({'name': f'{ACCOUNT_DATA["name"]}{i}'})

            created_units.append(
                unit_service.create(unit_data)
            )

        retrieved_units = unit_service.get_list(page, per_page)

        assert count_to_create == retrieved_units['total']

        created_units_skip = (page - 1) * per_page
        for i, retrieved_unit in enumerate(retrieved_units['units']):
            assert retrieved_unit.id == created_units[i + created_units_skip].id
            assert retrieved_unit.name == created_units[i + created_units_skip].name
