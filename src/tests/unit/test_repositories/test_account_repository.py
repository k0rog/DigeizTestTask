import pytest

from api.exceptions import AlreadyExistsException, DoesNotExistException
from api.models.account import Account


ACCOUNT_DATA = {
    'name': 'my_first_account',
}


class TestCreate:
    def test_is_id_returned(self, account_repository):
        account = account_repository.create(ACCOUNT_DATA)

        assert hasattr(account, 'id')

    def test_create(self, account_repository, session):
        account = account_repository.create(ACCOUNT_DATA)

        with session.begin() as session:
            storage_account = session.query(
                Account
            ).get(account.id)

        assert storage_account is not None
        assert storage_account.name == ACCOUNT_DATA['name']

    def test_for_duplicated_name(self, account_repository):
        account_repository.create(ACCOUNT_DATA)

        with pytest.raises(AlreadyExistsException) as exception_info:
            account_repository.create(ACCOUNT_DATA)

        assert exception_info.value.message == 'Account already exists!'


class TestUpdate:
    def test_for_one_field(self, account_repository, session):
        account = account_repository.create(ACCOUNT_DATA)

        update_data = {
            'name': 'updated_name'
        }

        account_repository.update(account.id, update_data)

        with session.begin() as session:
            storage_account = session.query(
                Account
            ).get(account.id)

        assert storage_account.name == update_data['name']

    def test_for_duplicated_name(self, account_repository):
        account_repository.create(ACCOUNT_DATA)

        second_account_data = ACCOUNT_DATA.copy()
        second_account_data.update({'name': 'second_account_name'})

        second_account = account_repository.create(second_account_data)

        update_data = {
            'name': ACCOUNT_DATA['name']
        }

        with pytest.raises(AlreadyExistsException) as exception_info:
            account_repository.update(second_account.id, update_data)

        assert exception_info.value.message == 'Account already exists!'


class TestDelete:
    def test_delete(self, account_repository, session):
        account = account_repository.create(ACCOUNT_DATA)

        is_deleted = account_repository.delete(account.id)

        assert is_deleted

        with session.begin() as session:
            assert session.query(
                Account
            ).get(account.id) is None

    def test_for_nonexistent_account(self, account_repository):
        is_deleted = account_repository.delete(1000)

        assert not is_deleted


class TestGet:
    def test_get(self, account_repository, session):
        account = account_repository.create(ACCOUNT_DATA)

        retrieved_account = account_repository.get(account.id)

        with session.begin() as session:
            storage_account = session.query(
                Account
            ).get(account.id)

        assert storage_account.name == retrieved_account.name

    def test_for_nonexistent_account(self, account_repository):
        with pytest.raises(DoesNotExistException) as exception_info:
            account_repository.get(1000)

        assert exception_info.value.message == 'Account does not exist!'


class TestGetList:
    @pytest.mark.parametrize(
        'count_to_create,page,per_page',
        (
                (10, 1, 5),
                (10, 2, 5),
                (10, 3, 3)
        )
    )
    def test_get_list(self, account_repository, count_to_create, page, per_page):
        created_accounts = []

        for i in range(count_to_create):
            account_data = ACCOUNT_DATA.copy()
            account_data.update({'name': f'{ACCOUNT_DATA["name"]}{i}'})

            created_accounts.append(
                account_repository.create(account_data)
            )

        retrieved_accounts = account_repository.get_list(page, per_page)

        assert count_to_create == retrieved_accounts['total']

        created_accounts_skip = (page - 1) * per_page
        for i, retrieved_account in enumerate(retrieved_accounts['accounts']):
            assert retrieved_account.id == created_accounts[i + created_accounts_skip].id
            assert retrieved_account.name == created_accounts[i + created_accounts_skip].name
