import pytest

from crm.users.models import User
from crm.events.models import Client, Event, Contract

from django.contrib.auth.models import Group, Permission
from django.test import Client as c

from datetime import date


@pytest.fixture
def client():
    client = c()
    return client


@pytest.fixture
def sales_member_one():
    """Créer un membre de l'équipe sales en BDD."""
    # créer un utilisateur
    sales_one = User.objects.create_user(
        username="sales1", password="vente1111"
    )

    # créer un groupe d'utilisateur 'support'
    sales_group, created = Group.objects.get_or_create(name='Sales')

    # ajouter des permissions au groupe
    perm_add_client = Permission.objects.get(codename='add_client')
    perm_change_client = Permission.objects.get(codename='change_client')
    perm_add_contract = Permission.objects.get(codename='add_contract')
    perm_change_contract = Permission.objects.get(codename='change_contract')
    perm_add_event = Permission.objects.get(codename='add_event')
    perm_change_event = Permission.objects.get(codename='change_event')
    sales_group.permissions.add(
        perm_add_client,
        perm_change_client,
        perm_add_contract,
        perm_change_contract,
        perm_add_event,
        perm_change_event,
    )

    # ajouter l'utilisateur au groupe
    sales_group.user_set.add(sales_one)

    return sales_one


@pytest.fixture
def sales_member_two():
    """Créer un membre de l'équipe sales en BDD."""
    # créer un utilisateur
    sales_two = User.objects.create_user(
        username="sales2", password="vente2222"
    )

    # créer un groupe d'utilisateur 'support'
    sales_group, created = Group.objects.get_or_create(name='Sales')

    # ajouter des permissions au groupe
    perm_add_client = Permission.objects.get(codename='add_client')
    perm_change_client = Permission.objects.get(codename='change_client')
    perm_add_contract = Permission.objects.get(codename='add_contract')
    perm_change_contract = Permission.objects.get(codename='change_contract')
    perm_add_event = Permission.objects.get(codename='add_event')
    perm_change_event = Permission.objects.get(codename='change_event')
    sales_group.permissions.add(
        perm_add_client,
        perm_change_client,
        perm_add_contract,
        perm_change_contract,
        perm_add_event,
        perm_change_event,
    )

    # ajouter l'utilisateur au groupe
    sales_group.user_set.add(sales_two)

    return sales_two


@pytest.fixture
def support_member_one():
    """Créer un membre de l'équipe sales en BDD."""
    # créer un utilisateur
    support_one = User.objects.create_user(
        username="support1", password="help1111"
    )

    # créer un groupe d'utilisateur 'support'
    sales_group, created = Group.objects.get_or_create(name='Support')

    # ajouter des permissions au groupe
    perm_view_client = Permission.objects.get(codename='view_client')
    perm_view_contract = Permission.objects.get(codename='view_contract')
    perm_view_event = Permission.objects.get(codename='view_event')
    perm_change_event = Permission.objects.get(codename='change_event')
    sales_group.permissions.add(
        perm_view_client,
        perm_view_contract,
        perm_view_event,
        perm_change_event,
    )

    # ajouter l'utilisateur au groupe
    sales_group.user_set.add(support_one)

    return support_one


@pytest.fixture
def support_member_two():
    """Créer un membre de l'équipe sales en BDD."""
    # créer un utilisateur
    support_two = User.objects.create_user(
        username="support2", password="help2222"
    )

    # créer un groupe d'utilisateur 'support'
    sales_group, created = Group.objects.get_or_create(name='Support')

    # ajouter des permissions au groupe
    perm_view_client = Permission.objects.get(codename='view_client')
    perm_view_contract = Permission.objects.get(codename='view_contract')
    perm_view_event = Permission.objects.get(codename='view_event')
    perm_change_event = Permission.objects.get(codename='change_event')
    sales_group.permissions.add(
        perm_view_client,
        perm_view_contract,
        perm_view_event,
        perm_change_event,
    )

    # ajouter l'utilisateur au groupe
    sales_group.user_set.add(support_two)


@pytest.fixture
def bdd_client(sales_member_one):
    client = Client.objects.create(
        sales_contact=sales_member_one,
        first_name='sam',
        last_name='idilbi',
        email='sam@test.com',
        phone='0222222222',
        mobile='0622222222',
        company_name='company two',
    )

    return client


@pytest.fixture
def bdd_contract(sales_member_one, bdd_client):

    contract = Contract.objects.create(
        sales_contact=sales_member_one,
        client=bdd_client,
        signed_status=False,
        amount=100.0,
        payment_due="2023-02-28",
    )

    return contract


@pytest.fixture
def bdd_event(bdd_client, support_member_one):
    event = Event.objects.create(
        client=bdd_client,
        support_contact=support_member_one,
        attendees=100,
        event_date="2023-02-25",
        notes="évènement de test",
        date_created="2023-02-23",
        date_updated="2023-02-23",
    )

    return event


@pytest.fixture
def login_as_sales_member(client):
    credentials = {"username": "sales1", "password": "vente1111"}
    response_login = client.post('api/login/', credentials)
    return response_login
