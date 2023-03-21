import pytest
from rest_framework.test import APIClient
from rest_framework.exceptions import ErrorDetail

from django.urls import reverse

from datetime import date


class TestCreateClient:
    client = APIClient()

    def login(self, username, password):
        credentials = {"username": username, "password": password}
        response_login = self.client.post(reverse('login'), credentials)
        token = response_login.data['access']

        return token

    @pytest.mark.django_db
    def test_create_client_as_sales_member(self, sales_member_one):
        """A sales member can create a client."""

        token = self.login(username="sales1", password="vente1111")

        client_data = {
            'first_name': 'sam',
            'last_name': 'idilbi',
            'email': 'sam@test.com',
            'phone': '0222222222',
            'mobile': '0622222222',
            'company_name': 'company two',
        }

        response = self.client.post(
            reverse('client-list'),
            client_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        date_updated = date.today().strftime('%Y-%m-%d')
        date_created = date.today().strftime('%Y-%m-%d')

        expected = {
            'id': 1,
            'first_name': 'sam',
            'last_name': 'idilbi',
            'email': 'sam@test.com',
            'phone': '0222222222',
            'mobile': '0622222222',
            'company_name': 'company two',
            'sales_contact': sales_member_one.id,
            'date_created': date_created,
            'date_updated': date_updated,
        }

        assert response.status_code == 201
        assert expected == response.data

    @pytest.mark.django_db
    def test_not_create_client_as_support_member(self, support_member_one):
        """A support member cannot create a client."""

        token = self.login(username="support1", password="help1111")

        client_data = {
            'first_name': 'sam',
            'last_name': 'idilbi',
            'email': 'sam@test.com',
            'phone': '0222222222',
            'mobile': '0622222222',
            'company_name': 'company two',
        }

        response = self.client.post(
            reverse('client-list'),
            client_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        assert response.status_code == 400


class TestGetClient:
    client = APIClient()

    def login(self, username, password):
        credentials = {"username": username, "password": password}
        response_login = self.client.post(reverse('login'), credentials)
        token = response_login.data['access']

        return token

    @pytest.mark.django_db
    def test_get_client_as_sales_member(self, client_one, sales_member_one):
        """A sales member can get any client."""

        token = self.login(username="sales1", password="vente1111")

        response = self.client.get(
            reverse('client-detail', args=[client_one.id]),
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        date_created = date.today().strftime('%Y-%m-%d')
        date_updated = date.today().strftime('%Y-%m-%d')

        expected = {
            'id': client_one.id,
            'first_name': 'sam',
            'last_name': 'idilbi',
            'email': 'sam@test.com',
            'phone': '0222222222',
            'mobile': '0622222222',
            'company_name': 'company two',
            'sales_contact': sales_member_one.id,
            'date_created': date_created,
            'date_updated': date_updated,
            'events': [],
            'contracts': [],
        }

        assert response.status_code == 200
        assert response.data == expected

    @pytest.mark.django_db
    def test_get_client_as_support_member(
        self, client_one, event_one, support_member_one, sales_member_one
    ):
        """A support member can get a client if he is
        the support contact of one of these events."""

        token = self.login(username="support1", password="help1111")

        response = self.client.get(
            reverse('client-detail', args=[client_one.id]),
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        date_created = date.today().strftime('%Y-%m-%d')
        date_updated = date.today().strftime('%Y-%m-%d')

        expected = {
            'id': client_one.id,
            'first_name': 'sam',
            'last_name': 'idilbi',
            'email': 'sam@test.com',
            'phone': '0222222222',
            'mobile': '0622222222',
            'company_name': 'company two',
            'sales_contact': sales_member_one.id,
            'date_created': date_created,
            'date_updated': date_updated,
            'events': [event_one.id],
            'contracts': [],
        }

        assert response.status_code == 200
        assert response.data == expected

    @pytest.mark.django_db
    def test_not_get_client_as_support_member(
        self, client_one, event_one, support_member_two
    ):
        """A support member cannot get a client if he is not
        the support contact of one of these events."""

        token = self.login(username="support2", password="help2222")

        response = self.client.get(
            reverse('client-detail', args=[1]),
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        expected = ErrorDetail(string='Not found.', code='not_found')

        assert response.data['detail'] == expected


class TestModifyClient:
    client = APIClient()

    def login(self, username, password):
        credentials = {"username": username, "password": password}
        response_login = self.client.post(reverse('login'), credentials)
        token = response_login.data['access']

        return token

    @pytest.mark.django_db
    def test_modify_client_as_sales_member(self, client_one, sales_member_one):
        """A sales member can modify a client if he is
        the sales contact of this client."""

        token = self.login(username="sales1", password="vente1111")

        client_data = {
            'first_name': 'sam modif',
            'last_name': 'idilbi modif',
            'email': 'sam_modif@test.com',
            'phone': '0222222221',
            'mobile': '0622222221',
            'company_name': 'company two modif',
        }

        response = self.client.put(
            reverse('client-detail', args=[client_one.id]),
            data=client_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        date_created = date.today().strftime('%Y-%m-%d')
        date_updated = date.today().strftime('%Y-%m-%d')

        expected = {
            'id': client_one.id,
            'first_name': 'sam modif',
            'last_name': 'idilbi modif',
            'email': 'sam_modif@test.com',
            'phone': '0222222221',
            'mobile': '0622222221',
            'company_name': 'company two modif',
            'sales_contact': sales_member_one.id,
            'date_created': date_created,
            'date_updated': date_updated,
        }

        assert response.status_code == 200
        assert response.data == expected

    @pytest.mark.django_db
    def test_not_modify_client_as_sales_member(
        self, client_one, sales_member_one, sales_member_two
    ):
        """A sales member cannot modify a client if he is not
        the sales contact of this client."""

        token = self.login(username="sales2", password="vente2222")

        client_data = {
            'first_name': 'sam modif',
            'last_name': 'idilbi modif',
            'email': 'sam_modif@test.com',
            'phone': '0222222221',
            'mobile': '0622222221',
            'company_name': 'company two modif',
            'sales_contact': sales_member_one.id,
        }

        response = self.client.put(
            reverse('client-detail', args=[client_one.id]),
            data=client_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        expected = ErrorDetail(
            string="You're not allowed because you're not the sales contact of the client.",
            code='permission_denied',
        )

        assert response.status_code == 403
        assert response.data['detail'] == expected

    @pytest.mark.django_db
    def test_not_modify_client_as_support_member(
        self, client_one, support_member_one, sales_member_one
    ):
        """A support member cannot modify a client."""

        token = self.login(username="support1", password="help1111")

        client_data = {
            'first_name': 'sam modif',
            'last_name': 'idilbi modif',
            'email': 'sam_modif@test.com',
            'phone': '0222222221',
            'mobile': '0622222221',
            'company_name': 'company two modif',
            'sales_contact': sales_member_one.id,
        }

        response = self.client.put(
            reverse('client-detail', args=[client_one.id]),
            data=client_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        assert response.status_code == 405
        assert (
            response.data['message']
            == 'You are not allowed because you are not a sales member.'
        )


class TestCreateContract:
    client = APIClient()

    def login(self, username, password):
        credentials = {"username": username, "password": password}
        response_login = self.client.post(reverse('login'), credentials)
        token = response_login.data['access']

        return token

    @pytest.mark.django_db
    def test_create_contract_as_sales_member(
        self, client_one, sales_member_one
    ):
        """A sales member can create a contract."""

        token = self.login(username="sales1", password="vente1111")

        contract_data = {
            'client': client_one.id,
            'signed_status': False,
            'amount': 50.0,
            'payment_due': '2023-02-28',
        }

        response = self.client.post(
            reverse('contract-list'),
            contract_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        date_updated = date.today().strftime('%Y-%m-%d')
        date_created = date.today().strftime('%Y-%m-%d')

        expected = {
            'id': 1,
            'client': client_one.id,
            'sales_contact': sales_member_one.id,
            'signed_status': False,
            'amount': 50.0,
            'date_created': date_created,
            'date_updated': date_updated,
            'payment_due': '2023-02-28',
        }

        assert response.status_code == 201
        assert expected == response.data

    @pytest.mark.django_db
    def test_not_create_contract_as_support_member(
        self, client_one, support_member_one
    ):
        """A support member cannot create a contract."""

        token = self.login(username="support1", password="help1111")

        contract_data = {
            'client': client_one.id,
            'signed_status': False,
            'amount': 50.0,
            'payment_due': '2023-02-28',
        }

        response = self.client.post(
            reverse('contract-list'),
            contract_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        assert response.status_code == 400
        assert (
            response.data['message']
            == 'You are not allowed. Only members of sales team can create a contract. '
        )


class TestGetContract:
    client = APIClient()

    def login(self, username, password):
        credentials = {"username": username, "password": password}
        response_login = self.client.post(reverse('login'), credentials)
        token = response_login.data['access']

        return token

    @pytest.mark.django_db
    def test_get_contract_as_sales_member(
        self, contract_one, client_one, sales_member_one
    ):
        """A sales member can get a contract if he is
        the sales contact of this contract."""

        token = self.login(username="sales1", password="vente1111")

        response = self.client.get(
            reverse('contract-detail', args=[contract_one.id]),
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        date_updated = date.today().strftime('%Y-%m-%d')
        date_created = date.today().strftime('%Y-%m-%d')

        expected = {
            'id': contract_one.id,
            'client': client_one.id,
            'sales_contact': sales_member_one.id,
            'signed_status': False,
            'amount': 100.0,
            'date_created': date_updated,
            'date_updated': date_created,
            'payment_due': "2023-02-28",
        }

        assert response.status_code == 200
        assert response.data == expected

    @pytest.mark.django_db
    def test_get_contract_as_support_member(
        self, contract_one, client_one, support_member_one, sales_member_one
    ):
        """A support member can get any contract."""

        token = self.login(username="support1", password="help1111")

        response = self.client.get(
            reverse('contract-detail', args=[contract_one.id]),
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        date_updated = date.today().strftime('%Y-%m-%d')
        date_created = date.today().strftime('%Y-%m-%d')

        expected = {
            'id': contract_one.id,
            'client': client_one.id,
            'sales_contact': sales_member_one.id,
            'signed_status': False,
            'amount': 100.0,
            'date_created': date_updated,
            'date_updated': date_created,
            'payment_due': "2023-02-28",
        }

        assert response.status_code == 200
        assert response.data == expected


class TestModifyContract:
    client = APIClient()

    def login(self, username, password):
        credentials = {"username": username, "password": password}
        response_login = self.client.post(reverse('login'), credentials)
        token = response_login.data['access']

        return token

    @pytest.mark.django_db
    def test_modify_contract_as_sales_member(
        self, contract_one, client_one, sales_member_one
    ):
        """A sales member can modify a contract if he is
        the sales contact of this contract."""

        token = self.login(username="sales1", password="vente1111")

        contract_data = {
            'client': client_one.id,
            'signed_status': True,
            'amount': 150.0,
            'payment_due': '2023-02-28',
        }

        response = self.client.put(
            reverse('contract-detail', args=[contract_one.id]),
            data=contract_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        date_updated = date.today().strftime('%Y-%m-%d')
        date_created = date.today().strftime('%Y-%m-%d')

        expected = {
            'id': contract_one.id,
            'client': client_one.id,
            'sales_contact': sales_member_one.id,
            'signed_status': True,
            'amount': 150.0,
            'date_created': date_updated,
            'date_updated': date_created,
            'payment_due': "2023-02-28",
        }

        assert response.status_code == 200
        assert response.data == expected

    @pytest.mark.django_db
    def test_not_modify_contract_as_sales_member(
        self, contract_one, client_one, sales_member_two
    ):
        """A sales member cannot modify a contract if he is not
        the sales contact of this contract."""

        token = self.login(username="sales2", password="vente2222")

        contract_data = {
            'client': client_one.id,
            'signed_status': True,
            'amount': 100.0,
            'payment_due': '2023-02-28',
        }

        response = self.client.put(
            reverse('contract-detail', args=[contract_one.id]),
            data=contract_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        expected = ErrorDetail(
            string="You're not allowed because you're not the sales contact of the client.",
            code='permission_denied',
        )

        assert response.data['detail'] == expected

    @pytest.mark.django_db
    def test_not_modify_contract_as_support_member(
        self, contract_one, client_one, support_member_one
    ):
        """A support member cannot modify a contract."""

        token = self.login(username="support1", password="help1111")

        contract_data = {
            'client': client_one.id,
            'signed_status': True,
            'amount': 100.0,
            'payment_due': '2023-02-28',
        }

        response = self.client.put(
            reverse('contract-detail', args=[contract_one.id]),
            data=contract_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        assert response.status_code == 400
        assert response.data['message'] == "You are not allowed."


class TestCreateEvent:
    client = APIClient()

    def login(self, username, password):
        credentials = {"username": username, "password": password}
        response_login = self.client.post(reverse('login'), credentials)
        token = response_login.data['access']

        return token

    @pytest.mark.django_db
    def test_create_event_as_sales_member(
        self, client_one, sales_member_one, support_member_one
    ):
        """A sales member can create an event."""

        token = self.login(username="sales1", password="vente1111")

        event_data = {
            'client': client_one.id,
            'support_contact': support_member_one.id,
            'attendees': 100,
            'event_date': '2023-02-28',
            'event_status': 1,
            'notes': 'test',
        }

        response = self.client.post(
            reverse('event-list'),
            event_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        date_updated = date.today().strftime('%Y-%m-%d')
        date_created = date.today().strftime('%Y-%m-%d')

        expected = {
            'client': client_one.id,
            'support_contact': support_member_one.id,
            'date_created': date_created,
            'date_updated': date_updated,
            'attendees': 100,
            'event_date': '2023-02-28',
            'event_status': 1,
            'notes': 'test',
        }

        del response.data['id']
        assert response.status_code == 201
        assert expected == response.data

    @pytest.mark.django_db
    def test_not_create_event_as_support_member(
        self, client_one, support_member_one
    ):
        """A support member cannot create an event."""

        token = self.login(username="support1", password="help1111")

        event_data = {
            'client': client_one.id,
            'support_contact': support_member_one.id,
            'attendees': 100,
            'event_date': '2023-02-28',
            'notes': 'test',
        }

        response = self.client.post(
            reverse('event-list'),
            event_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        assert response.status_code == 400
        assert (
            response.data['message']
            == "You are not allowed. Only members of sales team can create a contract."
        )


class TestGetEvent:
    client = APIClient()

    def login(self, username, password):
        credentials = {"username": username, "password": password}
        response_login = self.client.post(reverse('login'), credentials)
        token = response_login.data['access']

        return token

    @pytest.mark.django_db
    def test_get_event_as_sales_member(
        self, event_one, client_one, sales_member_one, support_member_one
    ):
        """A sales member can get an event if he is
        the sales contact of the associated client."""

        token = self.login(username="sales1", password="vente1111")

        response = self.client.get(
            reverse('event-detail', args=[event_one.id]),
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        date_updated = date.today().strftime('%Y-%m-%d')
        date_created = date.today().strftime('%Y-%m-%d')

        expected = {
            'id': event_one.id,
            'client': client_one.id,
            'support_contact': support_member_one.id,
            'date_created': date_created,
            'date_updated': date_updated,
            'attendees': 100,
            'event_date': '2023-02-25',
            'event_status': 1,
            'notes': 'évènement de test',
        }

        assert response.status_code == 200
        assert response.data == expected

    @pytest.mark.django_db
    def test_not_get_event_as_sales_member(
        self, event_one, client_one, sales_member_two, support_member_one
    ):
        """A sales member cannot get an event if he is not
        the sales contact of the associated client."""

        token = self.login(username="sales2", password="vente2222")

        response = self.client.get(
            reverse('event-detail', args=[event_one.id]),
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        expected = ErrorDetail(string='Not found.', code='not_found')

        assert response.data['detail'] == expected

    @pytest.mark.django_db
    def test_get_event_as_support_member(
        self, event_one, client_one, support_member_one
    ):
        """A support member can get an event if he is
        the support contact of the associated event."""

        token = self.login(username="support1", password="help1111")

        response = self.client.get(
            reverse('event-detail', args=[event_one.id]),
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        date_updated = date.today().strftime('%Y-%m-%d')
        date_created = date.today().strftime('%Y-%m-%d')

        expected = {
            'id': event_one.id,
            'client': client_one.id,
            'support_contact': support_member_one.id,
            'date_created': date_created,
            'date_updated': date_updated,
            'attendees': 100,
            'event_date': '2023-02-25',
            'event_status': 1,
            'notes': 'évènement de test',
        }

        assert response.status_code == 200
        assert response.data == expected

    @pytest.mark.django_db
    def test_not_get_event_as_support_member(
        self, event_one, client_one, support_member_two
    ):
        """A support member cannot get an event if he is not
        the support contact of this event."""

        token = self.login(username="support2", password="help2222")

        response = self.client.get(
            reverse('event-detail', args=[event_one.id]),
            HTTP_AUTHORIZATION=f'Bearer {token}',
            format='json',
        )

        expected = ErrorDetail(string='Not found.', code='not_found')

        assert response.data['detail'] == expected


class TestModifyEvent:
    client = APIClient()

    def login(self, username, password):
        credentials = {"username": username, "password": password}
        response_login = self.client.post(reverse('login'), credentials)
        token = response_login.data['access']

        return token

    @pytest.mark.django_db
    def test_modify_event_as_sales_member(
        self, event_one, client_one, sales_member_one, support_member_one
    ):
        """A sales member can modify an event if he is
        the sales contact of the associated client."""

        token = self.login(username="sales1", password="vente1111")

        event_data = {
            'client': client_one.id,
            'support_contact': support_member_one.id,
            'attendees': 150,
            'event_date': '2023-02-28',
            'notes': 'évènement de test modification',
        }

        response = self.client.put(
            reverse('event-detail', args=[event_one.id]),
            data=event_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        date_updated = date.today().strftime('%Y-%m-%d')
        date_created = date.today().strftime('%Y-%m-%d')

        expected = {
            'id': event_one.id,
            'client': client_one.id,
            'support_contact': support_member_one.id,
            'date_created': date_created,
            'date_updated': date_updated,
            'attendees': 150,
            'event_date': '2023-02-28',
            'event_status': 1,
            'notes': 'évènement de test modification',
        }

        assert response.data == expected

    @pytest.mark.django_db
    def test_not_modify_event_as_sales_member(
        self, event_one, client_one, sales_member_two, support_member_one
    ):
        """A support member can modify an event if he is
        the support contact of this event."""

        token = self.login(username="sales2", password="vente2222")

        event_data = {
            'client': client_one.id,
            'support_contact': support_member_one.id,
            'attendees': 150,
            'event_date': '2023-02-28',
            'notes': 'évènement de test modification',
        }

        response = self.client.put(
            reverse('event-detail', args=[event_one.id]),
            data=event_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        expected = ErrorDetail(
            string="You're not allowed because you're not the sales contact of the client.",
            code='permission_denied',
        )

        assert response.status_code == 403
        assert response.data['detail'] == expected

    @pytest.mark.django_db
    def test_modify_event_as_support_member(
        self, event_one, client_one, support_member_one
    ):
        """A support member can modify an event if he is
        the support contact of this event"""

        token = self.login(username="support1", password="help1111")

        event_data = {
            'client': client_one.id,
            'support_contact': support_member_one.id,
            'attendees': 150,
            'event_date': '2023-02-28',
            'notes': 'évènement de test modification',
        }

        response = self.client.put(
            reverse('event-detail', args=[event_one.id]),
            data=event_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        date_updated = date.today().strftime('%Y-%m-%d')
        date_created = date.today().strftime('%Y-%m-%d')

        expected = {
            'id': event_one.id,
            'client': client_one.id,
            'support_contact': support_member_one.id,
            'date_created': date_created,
            'date_updated': date_updated,
            'attendees': 150,
            'event_date': '2023-02-28',
            'event_status': 1,
            'notes': 'évènement de test modification',
        }

        assert response.data == expected

    @pytest.mark.django_db
    def test_not_modify_event_as_support_member(
        self, event_one, client_one, support_member_one, support_member_two
    ):
        """A support member can modify an event if he is
        the support contact of this event."""

        token = self.login(username="support2", password="help2222")

        event_data = {
            'client': client_one.id,
            'support_contact': support_member_one.id,
            'attendees': 150,
            'event_date': '2023-02-28',
            'notes': 'évènement de test modification',
        }

        response = self.client.put(
            reverse('event-detail', args=[event_one.id]),
            data=event_data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        expected = ErrorDetail(
            string="You're not allowed because you're not the support contact.",
            code='permission_denied',
        )

        assert response.status_code == 403
        assert response.data['detail'] == expected
