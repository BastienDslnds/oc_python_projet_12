import pytest
from rest_framework.test import APIClient
from rest_framework.exceptions import ErrorDetail

from django.urls import reverse

from datetime import date


client = APIClient()


@pytest.mark.django_db
def test_create_client_as_sales_member(sales_member_one):
    """A sales member can create a client."""

    credentials = {"username": "sales1", "password": "vente1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    client_data = {
        'first_name': 'sam',
        'last_name': 'idilbi',
        'email': 'sam@test.com',
        'phone': '0222222222',
        'mobile': '0622222222',
        'company_name': 'company two',
    }

    response = client.post(
        reverse('client-list'),
        client_data,
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    date_updated = date.today().strftime('%Y-%m-%d')
    date_created = date.today().strftime('%Y-%m-%d')

    # convertir le format datetime en format string

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
def test_not_create_client_as_support_member(
    support_member_one, sales_member_one
):
    """A support member cannot create a client."""

    credentials = {"username": "support1", "password": "help1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    client_data = {
        'first_name': 'sam',
        'last_name': 'idilbi',
        'email': 'sam@test.com',
        'phone': '0222222222',
        'mobile': '0622222222',
        'company_name': 'company two',
    }

    response = client.post(
        reverse('client-list'),
        client_data,
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_get_client_as_sales_member(bdd_client, sales_member_one):
    """A sales member can get any client."""

    credentials = {"username": "sales1", "password": "vente1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    response = client.get(
        reverse('client-detail', args=[1]),
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    date_created = date.today().strftime('%Y-%m-%d')
    date_updated = date.today().strftime('%Y-%m-%d')

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
        'events': [],
        'contracts': [],
    }

    assert response.status_code == 200
    assert response.data == expected


@pytest.mark.django_db
def test_get_client_as_support_member(
    bdd_event, sales_member_one, support_member_one
):
    """A support member can get a client if he is
    the support contact of one of these events."""

    credentials = {"username": "support1", "password": "help1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    response = client.get(
        reverse('client-detail', args=[1]),
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    date_created = date.today().strftime('%Y-%m-%d')
    date_updated = date.today().strftime('%Y-%m-%d')

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
        'events': [1],
        'contracts': [],
    }

    assert response.status_code == 200
    assert response.data == expected


@pytest.mark.django_db
def test_not_get_client_as_support_member(bdd_event, support_member_two):
    """A support member cannot get a client if he is not
    the support contact of one of these events."""

    credentials = {"username": "support2", "password": "help2222"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    response = client.get(
        reverse('client-detail', args=[1]),
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    expected = ErrorDetail(string='Not found.', code='not_found')

    assert response.data['detail'] == expected


@pytest.mark.django_db
def test_modify_client_as_sales_member(bdd_client, sales_member_one):
    """A sales member can modify a client if he is
    the sales contact of this client."""

    credentials = {"username": "sales1", "password": "vente1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    client_data = {
        'first_name': 'sam modif',
        'last_name': 'idilbi modif',
        'email': 'sam_modif@test.com',
        'phone': '0222222221',
        'mobile': '0622222221',
        'company_name': 'company two modif',
        'sales_contact': sales_member_one.id,
    }

    response = client.put(
        reverse('client-detail', args=[1]),
        data=client_data,
        HTTP_AUTHORIZATION=f'Bearer {token}',
    )

    date_created = date.today().strftime('%Y-%m-%d')
    date_updated = date.today().strftime('%Y-%m-%d')

    expected = {
        'id': 1,
        'first_name': 'sam modif',
        'last_name': 'idilbi modif',
        'email': 'sam_modif@test.com',
        'phone': '0222222221',
        'mobile': '0622222221',
        'company_name': 'company two modif',
        'sales_contact': 1,
        'date_created': date_created,
        'date_updated': date_updated,
    }

    assert response.status_code == 200
    assert response.data == expected


@pytest.mark.django_db
def test_not_modify_client_as_sales_member(bdd_client, sales_member_two):
    """A sales member cannot modify a client if he is not
    the sales contact of this client."""

    credentials = {"username": "sales2", "password": "vente2222"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    client_data = {
        'first_name': 'sam modif',
        'last_name': 'idilbi modif',
        'email': 'sam_modif@test.com',
        'phone': '0222222221',
        'mobile': '0622222221',
        'company_name': 'company two modif',
        'sales_contact': 1,
    }

    response = client.put(
        reverse('client-detail', args=[1]),
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
def test_not_modify_client_as_support_member(bdd_client, support_member_one):
    """A support member cannot modify a client."""

    credentials = {"username": "support1", "password": "help1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    client_data = {
        'first_name': 'sam modif',
        'last_name': 'idilbi modif',
        'email': 'sam_modif@test.com',
        'phone': '0222222221',
        'mobile': '0622222221',
        'company_name': 'company two modif',
        'sales_contact': 1,
    }

    response = client.put(
        reverse('client-detail', args=[1]),
        data=client_data,
        HTTP_AUTHORIZATION=f'Bearer {token}',
    )

    assert response.status_code == 405
    assert (
        response.data['message']
        == 'You are not allowed because you are not a sales member.'
    )


@pytest.mark.django_db
def test_create_contract_as_sales_member(bdd_client, sales_member_one):
    """A sales member can create a contract."""

    credentials = {"username": "sales1", "password": "vente1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    contract_data = {
        'client': bdd_client.id,
        'signed_status': False,
        'amount': 50.0,
        'payment_due': '2023-02-28',
    }

    response = client.post(
        reverse('contract-list'),
        contract_data,
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    date_updated = date.today().strftime('%Y-%m-%d')
    date_created = date.today().strftime('%Y-%m-%d')

    expected = {
        'id': 1,
        'client': 1,
        'sales_contact': 1,
        'signed_status': False,
        'amount': 50.0,
        'date_created': date_created,
        'date_updated': date_updated,
        'payment_due': '2023-02-28',
    }

    assert response.status_code == 201
    assert expected == response.data


@pytest.mark.django_db
def test_not_create_contract_as_support_member(bdd_client, support_member_one):
    """A support member cannot create a contract."""

    credentials = {"username": "support1", "password": "help1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    contract_data = {
        'client': bdd_client.id,
        'signed_status': False,
        'amount': 50.0,
        'payment_due': '2023-02-28',
    }

    response = client.post(
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


@pytest.mark.django_db
def test_get_contract_as_sales_member(bdd_contract, sales_member_one):
    """A sales member can get a contract if he is
    the sales contact of this contract."""

    credentials = {"username": "sales1", "password": "vente1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    response = client.get(
        reverse('contract-detail', args=[1]),
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    date_updated = date.today().strftime('%Y-%m-%d')
    date_created = date.today().strftime('%Y-%m-%d')

    expected = {
        'id': 1,
        'client': 1,
        'sales_contact': 1,
        'signed_status': False,
        'amount': 100.0,
        'date_created': date_updated,
        'date_updated': date_created,
        'payment_due': "2023-02-28",
    }

    assert response.status_code == 200
    assert response.data == expected


@pytest.mark.django_db
def test_get_contract_as_support_member(bdd_contract, support_member_one):
    """A support member can get any contract."""

    credentials = {"username": "support1", "password": "help1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    response = client.get(
        reverse('contract-detail', args=[1]),
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    date_updated = date.today().strftime('%Y-%m-%d')
    date_created = date.today().strftime('%Y-%m-%d')

    expected = {
        'id': 1,
        'client': 1,
        'sales_contact': 1,
        'signed_status': False,
        'amount': 100.0,
        'date_created': date_updated,
        'date_updated': date_created,
        'payment_due': "2023-02-28",
    }

    assert response.status_code == 200
    assert response.data == expected


@pytest.mark.django_db
def test_modify_contract_as_sales_member(bdd_contract, sales_member_one):
    """A sales member can modify a contract if he is
    the sales contact of this contract."""

    credentials = {"username": "sales1", "password": "vente1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    contract_data = {
        'client': 1,
        'signed_status': True,
        'amount': 150.0,
        'payment_due': '2023-02-28',
    }

    response = client.put(
        reverse('contract-detail', args=[1]),
        data=contract_data,
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    date_updated = date.today().strftime('%Y-%m-%d')
    date_created = date.today().strftime('%Y-%m-%d')

    expected = {
        'id': 1,
        'client': 1,
        'sales_contact': 1,
        'signed_status': True,
        'amount': 150.0,
        'date_created': date_updated,
        'date_updated': date_created,
        'payment_due': "2023-02-28",
    }

    print(response)

    assert response.status_code == 200
    assert response.data == expected


@pytest.mark.django_db
def test_not_modify_contract_as_sales_member(bdd_contract, sales_member_two):
    """A sales member cannot modify a contract if he is not
    the sales contact of this contract."""

    credentials = {"username": "sales2", "password": "vente2222"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    contract_data = {
        'client': 1,
        'signed_status': True,
        'amount': 100.0,
        'payment_due': '2023-02-28',
    }

    response = client.put(
        reverse('contract-detail', args=[1]),
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
    bdd_contract, support_member_one
):
    """A support member cannot modify a contract."""

    credentials = {"username": "support1", "password": "help1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    contract_data = {
        'client': 1,
        'signed_status': True,
        'amount': 100.0,
        'payment_due': '2023-02-28',
    }

    response = client.put(
        reverse('contract-detail', args=[1]),
        data=contract_data,
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    assert response.status_code == 400
    assert response.data['message'] == "You are not allowed."


@pytest.mark.django_db
def test_create_event_as_sales_member(
    bdd_client, support_member_one, bdd_event_status
):
    """A sales member can create an event."""

    credentials = {"username": "sales1", "password": "vente1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    event_data = {
        'client': bdd_client.id,
        'support_contact': support_member_one.id,
        'attendees': 100,
        'event_date': '2023-02-28',
        'event_status': 2,
        'notes': 'test',
    }

    response = client.post(
        reverse('event-list'),
        event_data,
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    date_updated = date.today().strftime('%Y-%m-%d')
    date_created = date.today().strftime('%Y-%m-%d')

    expected = {
        'id': 1,
        'client': 1,
        'support_contact': 2,
        'date_created': date_created,
        'date_updated': date_updated,
        'attendees': 100,
        'event_date': '2023-02-28',
        'event_status': 2,
        'notes': 'test',
    }

    assert response.status_code == 201
    assert expected == response.data


@pytest.mark.django_db
def test_not_create_event_as_support_member(bdd_client, support_member_one):
    """A support member cannot create an event."""

    credentials = {"username": "support1", "password": "help1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    event_data = {
        'client': bdd_client.id,
        'support_contact': support_member_one.id,
        'attendees': 100,
        'event_date': '2023-02-28',
        'notes': 'test',
    }

    response = client.post(
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


@pytest.mark.django_db
def test_get_event_as_sales_member(bdd_event, bdd_client, support_member_one):
    """A sales member can get an event if he is
    the sales contact of the associated client."""

    credentials = {"username": "sales1", "password": "vente1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    response = client.get(
        reverse('event-detail', args=[1]),
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    date_updated = date.today().strftime('%Y-%m-%d')
    date_created = date.today().strftime('%Y-%m-%d')

    expected = {
        'id': 1,
        'client': bdd_client.id,
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
def test_get_event_as_support_member(
    bdd_event, bdd_client, support_member_one
):
    """A support member can get any event."""

    credentials = {"username": "support1", "password": "help1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    response = client.get(
        reverse('event-detail', args=[1]),
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    date_updated = date.today().strftime('%Y-%m-%d')
    date_created = date.today().strftime('%Y-%m-%d')

    expected = {
        'id': 1,
        'client': bdd_client.id,
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
def test_modify_event_as_sales_member(
    bdd_event, bdd_client, sales_member_one, support_member_one
):
    """A sales member can modify an event if he is
    the sales contact of the associated client."""

    credentials = {"username": "sales1", "password": "vente1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    event_data = {
        'client': bdd_client.id,
        'support_contact': support_member_one.id,
        'attendees': 150,
        'event_date': '2023-02-28',
        'notes': 'évènement de test modification',
    }

    response = client.put(
        reverse('event-detail', args=[1]),
        data=event_data,
        HTTP_AUTHORIZATION=f'Bearer {token}',
        format='json',
    )

    date_updated = date.today().strftime('%Y-%m-%d')
    date_created = date.today().strftime('%Y-%m-%d')

    expected = {
        'id': 1,
        'client': bdd_client.id,
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
    bdd_event, bdd_client, sales_member_two, support_member_one
):
    """A support member can modify an event if he is
    the support contact of this event."""

    credentials = {"username": "sales2", "password": "vente2222"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    event_data = {
        'client': bdd_client.id,
        'support_contact': support_member_one.id,
        'attendees': 150,
        'event_date': '2023-02-28',
        'notes': 'évènement de test modification',
    }

    response = client.put(
        reverse('event-detail', args=[1]),
        data=event_data,
        HTTP_AUTHORIZATION=f'Bearer {token}',
    )

    print(response.data)
    expected = ErrorDetail(
        string="You're not allowed because you're not the sales contact of the client.",
        code='permission_denied',
    )

    assert response.status_code == 403
    assert response.data['detail'] == expected


@pytest.mark.django_db
def test_modify_event_as_support_member(
    bdd_event, bdd_client, support_member_one
):
    """A support member can modify an event if he is
    the support contact of this event"""

    credentials = {"username": "support1", "password": "help1111"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    event_data = {
        'client': bdd_client.id,
        'support_contact': support_member_one.id,
        'attendees': 150,
        'event_date': '2023-02-28',
        'notes': 'évènement de test modification',
    }

    date_updated = date.today().strftime('%Y-%m-%d')
    date_created = date.today().strftime('%Y-%m-%d')

    expected = {
        'id': 1,
        'client': bdd_client.id,
        'support_contact': support_member_one.id,
        'date_created': date_created,
        'date_updated': date_updated,
        'attendees': 150,
        'event_date': '2023-02-28',
        'event_status': 1,
        'notes': 'évènement de test modification',
    }

    response = client.put(
        reverse('event-detail', args=[1]),
        data=event_data,
        HTTP_AUTHORIZATION=f'Bearer {token}',
    )

    assert response.data == expected


@pytest.mark.django_db
def test_not_modify_event_as_support_member(
    bdd_event, bdd_client, support_member_one, support_member_two
):
    """A support member can modify an event if he is
    the support contact of this event."""

    credentials = {"username": "support2", "password": "help2222"}
    response_login = client.post(reverse('login'), credentials)
    token = response_login.data['access']

    event_data = {
        'client': bdd_client.id,
        'support_contact': support_member_one.id,
        'attendees': 150,
        'event_date': '2023-02-28',
        'notes': 'évènement de test modification',
    }

    response = client.put(
        reverse('event-detail', args=[1]),
        data=event_data,
        HTTP_AUTHORIZATION=f'Bearer {token}',
    )

    print(response.data)
    expected = ErrorDetail(
        string="You're not allowed because you're not the support contact.",
        code='permission_denied',
    )

    assert response.status_code == 403
    assert response.data['detail'] == expected
