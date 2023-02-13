import pytest
from http import HTTPStatus

from api.models.mall import Mall


class TestCreate:
    URL = '/api/malls/'

    def test_is_id_returned(self, client, permanent_mall_data):
        response = client.post(self.URL, json=permanent_mall_data)

        assert response.status_code == HTTPStatus.CREATED
        assert 'id' in response.json

    def test_create(self, client, permanent_session, permanent_mall_data):
        response = client.post(self.URL, json=permanent_mall_data)
        assert response.status_code == HTTPStatus.CREATED

        with permanent_session.begin() as session:
            storage_mall = session.query(
                Mall
            ).get(response.json['id'])

        assert storage_mall is not None
        assert storage_mall.name == permanent_mall_data['name']

    def test_for_duplicated_name(self, client, permanent_mall_data):
        client.post(self.URL, json=permanent_mall_data)
        response = client.post(self.URL, json=permanent_mall_data)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert 'error' in response.json
        assert response.json['error'] == 'Mall already exists!'

    @pytest.mark.parametrize(
        'field,value',
        (
                ('name', 123),
        ))
    def test_with_invalid_data(self, client, field, value, permanent_mall_data):
        permanent_mall_data[field] = value

        response = client.post(self.URL, json=permanent_mall_data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert 'errors' in response.json
        assert response.json['errors']['json'][field] == ['Not a valid string.']


class TestUpdate:
    URL = '/api/malls/'

    def test_update(self, client, permanent_session, permanent_mall_data):
        mall_id = client.post(self.URL, json=permanent_mall_data).json['id']

        update_data = {
            'name': 'updated_name',
        }

        response = client.patch(
            self.URL + str(mall_id),
            json=update_data
        )

        with permanent_session.begin() as session:
            storage_mall = session.query(
                Mall
            ).get(mall_id)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert storage_mall.name == update_data['name']

    def test_for_duplicated_name(self, client, permanent_mall_data):
        client.post(self.URL, json=permanent_mall_data)

        second_permanent_mall_data = permanent_mall_data.copy()
        second_permanent_mall_data.update({
            'name': 'second_mall_name'
        })
        response = client.post(self.URL, json=second_permanent_mall_data)

        update_response = client.patch(
            self.URL + str(response.json['id']),
            json={'name': permanent_mall_data['name']}
        )

        assert update_response.status_code == HTTPStatus.BAD_REQUEST
        assert 'error' in update_response.json
        assert update_response.json['error'] == 'Mall already exists!'

    @pytest.mark.parametrize(
        'field,value',
        (
                ('name', 123),
        ))
    def test_with_invalid_data(self, client, permanent_mall_data, field, value):
        mall_id = client.post(self.URL, json=permanent_mall_data).json['id']

        update_data = {field: value}

        response = client.patch(self.URL + str(mall_id), json=update_data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert 'errors' in response.json
        assert response.json['errors']['json'][field] == ['Not a valid string.']


class TestDelete:
    URL = '/api/malls/'

    def test_delete(self, client, permanent_session, permanent_mall_data):
        mall_id = client.post(self.URL, json=permanent_mall_data).json['id']

        response = client.delete(self.URL + str(mall_id))

        assert response.status_code == HTTPStatus.NO_CONTENT

        with permanent_session.begin() as session:
            assert session.query(
                Mall.id
            ).filter_by(id=mall_id).first() is None

    def test_delete_nonexistent_customer(self, client):
        response = client.delete(self.URL + str(10000))

        assert response.status_code == HTTPStatus.NO_CONTENT


class TestGet:
    URL = '/api/malls/'

    def test_get(self, client, permanent_mall_data):
        mall_id = client.post(self.URL, json=permanent_mall_data).json['id']

        retrieved_mall = client.get(
            self.URL + str(mall_id)
        )

        assert retrieved_mall.status_code == HTTPStatus.OK
        assert retrieved_mall.json['name'] == permanent_mall_data['name']
        assert retrieved_mall.json['id'] == mall_id

    def test_for_nonexistent_mall(self, client):
        response = client.get(
            self.URL + str(1000)
        )

        assert response.status_code == 404
        assert 'error' in response.json
        assert response.json['error'] == 'Mall does not exist!'


class TestGetList:
    URL = '/api/malls/'

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
    URL = '/api/malls/bulk'

    def test_bulk_create(self, client, permanent_session, permanent_account):
        data = {'malls': [{
            'name': 'first_mall',
            'account_id': permanent_account.id
        }, {
            'name': 'second_mall',
            'account_id': permanent_account.id
        }]}

        response = client.post(self.URL, json=data)

        assert response.status_code == HTTPStatus.CREATED

        with permanent_session.begin() as session:
            assert session.query(
                Mall
            ).filter(
                Mall.name.in_(
                    [mall['name'] for mall in data['malls']]
                )
            ).count() == len(data['malls'])

    def test_bulk_create_with_duplicated_data(self, client, permanent_account):
        data = {'malls': [{
            'name': 'first_mall',
            'account_id': permanent_account.id
        }, {
            'name': 'second_mall',
            'account_id': permanent_account.id
        }]}

        client.post(self.URL, json=data)

        response = client.post(self.URL, json=data)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert 'error' in response.json
        assert response.json['error'] == 'One or more malls already exist!'
