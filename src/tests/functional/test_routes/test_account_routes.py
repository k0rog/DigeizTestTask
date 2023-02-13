import pytest
from http import HTTPStatus

from api.models.account import Account


class TestCreate:
    URL = '/api/accounts/'

    def test_is_id_returned(self, client, permanent_account_data):
        response = client.post(self.URL, json=permanent_account_data)

        assert response.status_code == HTTPStatus.CREATED
        assert 'id' in response.json

    def test_create(self, client, permanent_session, permanent_account_data):
        response = client.post(self.URL, json=permanent_account_data)
        assert response.status_code == HTTPStatus.CREATED

        with permanent_session.begin() as session:
            storage_account = session.query(
                Account
            ).get(response.json['id'])

        assert storage_account is not None
        assert storage_account.name == permanent_account_data['name']

    def test_for_duplicated_name(self, client, permanent_account_data):
        client.post(self.URL, json=permanent_account_data)
        response = client.post(self.URL, json=permanent_account_data)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert 'error' in response.json
        assert response.json['error'] == 'Account already exists!'

    @pytest.mark.parametrize(
        'field,value',
        (
                ('name', 123),
        ))
    def test_with_invalid_data(self, client, field, value, permanent_account_data):
        permanent_account_data[field] = value

        response = client.post(self.URL, json=permanent_account_data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert 'errors' in response.json
        assert response.json['errors']['json'][field] == ['Not a valid string.']


class TestUpdate:
    URL = '/api/accounts/'

    def test_update(self, client, permanent_session, permanent_account_data):
        account_id = client.post(self.URL, json=permanent_account_data).json['id']

        update_data = {
            'name': 'updated_name',
        }

        response = client.patch(
            self.URL + str(account_id),
            json=update_data
        )

        with permanent_session.begin() as session:
            storage_account = session.query(
                Account
            ).get(account_id)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert storage_account.name == update_data['name']

    def test_for_duplicated_name(self, client, permanent_account_data):
        client.post(self.URL, json=permanent_account_data)

        second_account_data = permanent_account_data.copy()
        second_account_data.update({
            'name': 'second_account_name'
        })
        response = client.post(self.URL, json=second_account_data)

        update_response = client.patch(
            self.URL + str(response.json['id']),
            json={'name': permanent_account_data['name']}
        )

        assert update_response.status_code == HTTPStatus.BAD_REQUEST
        assert 'error' in update_response.json
        assert update_response.json['error'] == 'Account already exists!'

    @pytest.mark.parametrize(
        'field,value',
        (
                ('name', 123),
        ))
    def test_with_invalid_data(self, client, permanent_account_data, field, value):
        account_id = client.post(self.URL, json=permanent_account_data).json['id']

        update_data = {field: value}

        response = client.patch(self.URL + str(account_id), json=update_data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert 'errors' in response.json
        assert response.json['errors']['json'][field] == ['Not a valid string.']


class TestDelete:
    URL = '/api/accounts/'

    def test_delete(self, client, permanent_session, permanent_account_data):
        account_id = client.post(self.URL, json=permanent_account_data).json['id']

        response = client.delete(self.URL + str(account_id))

        assert response.status_code == HTTPStatus.NO_CONTENT

        with permanent_session.begin() as session:
            assert session.query(
                Account.id
            ).filter_by(id=account_id).first() is None

    def test_delete_nonexistent_customer(self, client):
        response = client.delete(self.URL + str(10000))

        assert response.status_code == HTTPStatus.NO_CONTENT


class TestGet:
    URL = '/api/accounts/'

    def test_get(self, client, permanent_account_data):
        account_id = client.post(self.URL, json=permanent_account_data).json['id']

        retrieved_account = client.get(
            self.URL + str(account_id)
        )

        assert retrieved_account.status_code == HTTPStatus.OK
        assert retrieved_account.json['name'] == permanent_account_data['name']
        assert retrieved_account.json['id'] == account_id

    def test_for_nonexistent_account(self, client):
        response = client.get(
            self.URL + str(1000)
        )

        assert response.status_code == 404
        assert 'error' in response.json
        assert response.json['error'] == 'Account does not exist!'


class TestGetList:
    URL = '/api/accounts/'

    def test_with_wrong_page(self, client):
        response = client.get(
            '{}?page={}&per_page={}'.format(self.URL, -1, 10)
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert 'errors' in response.json
        assert response.json['errors']['querystring']['page'] == \
               ['Wrong page value! Try value > 1.']

    @pytest.mark.parametrize('per_page', (100, -1))
    def test_with_wrong_per_page(self, client, per_page):
        response = client.get(
            '{}?page={}&per_page={}'.format(self.URL, 1, per_page)
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert 'errors' in response.json
        assert response.json['errors']['querystring']['per_page'] == \
               ['Must be greater than or equal to 1 and less than or equal to 50.']


class TestBulkCreate:
    URL = '/api/accounts/bulk'

    def test_bulk_create(self, client, permanent_session):
        data = {'accounts': [{
            'name': 'first_account',
        }, {
            'name': 'second_account'
        }]}

        client.post(self.URL, json=data)

        with permanent_session.begin() as session:
            assert session.query(
                Account
            ).filter(
                Account.name.in_(
                    [account['name'] for account in data['accounts']]
                )
            ).count() == len(data['accounts'])

    def test_bulk_create_with_duplicated_data(self, client):
        data = {'accounts': [{
            'name': 'first_account',
        }, {
            'name': 'second_account'
        }]}

        client.post(self.URL, json=data)

        response = client.post(self.URL, json=data)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert 'error' in response.json
        assert response.json['error'] == 'One or more accounts already exist!'
