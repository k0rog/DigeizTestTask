import pytest

from api.exceptions import AlreadyExistsException, DoesNotExistException
from api.models.account import Account



class TestCreate:
    def test_is_id_returned(self, account_service, account_data):
        account = account_service.create(account_data)

        assert hasattr(account, 'id')

    def test_create(self, account_service, session, account_data):
        account = account_service.create(account_data)

        with session.begin() as session:
            storage_account = session.query(
                Account
            ).get(account.id)

        assert storage_account is not None
        assert storage_account.name == account_data['name']

    def test_for_duplicated_name(self, account_service, account_data):
        account_service.create(account_data)

        with pytest.raises(AlreadyExistsException) as exception_info:
            account_service.create(account_data)

        assert exception_info.value.message == 'Account already exists!'


class TestUpdate:
    def test_for_one_field(self, account_service, session, account_data):
        account = account_service.create(account_data)

        update_data = {
            'name': 'updated_name'
        }

        account_service.update(account.id, update_data)

        with session.begin() as session:
            storage_account = session.query(
                Account
            ).get(account.id)

        assert storage_account.name == update_data['name']

    def test_for_duplicated_name(self, account_service, account_data):
        account_service.create(account_data)

        second_account_data = account_data.copy()
        second_account_data.update({'name': 'second_account_name'})

        second_account = account_service.create(second_account_data)

        update_data = {
            'name': account_data['name']
        }

        with pytest.raises(AlreadyExistsException) as exception_info:
            account_service.update(second_account.id, update_data)

        assert exception_info.value.message == 'Account already exists!'


class TestDelete:
    def test_delete(self, account_service, session, account_data):
        account = account_service.create(account_data)

        is_deleted = account_service.delete(account.id)

        assert is_deleted

        with session.begin() as session:
            assert session.query(
                Account
            ).get(account.id) is None

    def test_for_nonexistent_account(self, account_service):
        is_deleted = account_service.delete(1000)

        assert not is_deleted


class TestGet:
    def test_get(self, account_service, session, account_data):
        account = account_service.create(account_data)

        retrieved_account = account_service.get(account.id)

        with session.begin() as session:
            storage_account = session.query(
                Account
            ).get(account.id)

        assert storage_account.name == retrieved_account.name

    def test_for_nonexistent_account(self, account_service):
        with pytest.raises(DoesNotExistException) as exception_info:
            account_service.get(1000)

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
    def test_get_list(self, account_service, account_data, count_to_create, page, per_page):
        created_accounts = []

        for i in range(count_to_create):
            account_data = account_data.copy()
            account_data.update({'name': f'{account_data["name"]}{i}'})

            created_accounts.append(
                account_service.create(account_data)
            )

        retrieved_accounts = account_service.get_list(page, per_page)

        assert count_to_create == retrieved_accounts['total']

        created_accounts_skip = (page - 1) * per_page
        for i, retrieved_account in enumerate(retrieved_accounts['accounts']):
            assert retrieved_account.id == created_accounts[i + created_accounts_skip].id
            assert retrieved_account.name == created_accounts[i + created_accounts_skip].name


class TestBulkCreate:
    def test_bulk_create(self, account_service, session):
        data = {'accounts': [{
            'name': 'first_account',
        }, {
            'name': 'second_account'
        }]}

        account_service.bulk_create(data)

        with session.begin() as session:
            assert session.query(
                Account
            ).filter(
                Account.name.in_(
                    [account['name'] for account in data['accounts']]
                )
            ).count() == len(data['accounts'])

    def test_bulk_create_with_duplicated_data(self, account_service):
        data = {'accounts': [{
            'name': 'first_account',
        }, {
            'name': 'second_account'
        }]}

        account_service.bulk_create(data)

        with pytest.raises(AlreadyExistsException) as exception_info:
            account_service.bulk_create(data)

        assert exception_info.value.message == 'One or more accounts already exist!'
