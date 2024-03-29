from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
import logging

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from datetime import date

from .permissions import IsSalesContact, IsSupportContact, HasActiveContract

from .serializers import (
    ClientListSerializer,
    ClientDetailSerializer,
    ContractSerializer,
    EventSerializer,
)
from .models import Client, Contract, Event
from .filters import ContractFilter

logger = logging.getLogger(__name__)


class ClientViewset(ModelViewSet):
    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer

    permission_classes = [IsAuthenticated, IsSalesContact]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_name', 'email']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_permissions(self):
        if self.request.method in ['PUT']:
            return [IsSalesContact()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.groups.filter(name='Support'):
            logger.debug("GET client(s) by support user: OK")
            return Client.objects.filter(
                events__support_contact=self.request.user.id
            )
        elif self.request.user.groups.filter(name='Sales'):
            logger.debug("GET client(s) by sales user: OK")
            return Client.objects.filter(sales_contact=self.request.user.id)
        return Client.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.has_perm('events.add_client'):
            client = request.data.copy()
            client['sales_contact'] = user.id
            client["date_updated"] = date.today()
            serializer = self.get_serializer(data=client)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.debug("POST client: OK")
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            logger.debug(
                "POST client: You don't have the permission to add a client."
            )
            return Response(
                {'message': "You are not allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.has_perm('events.change_client'):
            client = get_object_or_404(Client, pk=self.kwargs['pk'])
            self.check_object_permissions(request, client)
            data = request.data.copy()
            data['sales_contact'] = user.id
            data["date_updated"] = date.today()
            serializer = ClientListSerializer(client, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.debug("PUT client: OK")
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            logger.debug(
                "PUT client: You don't have the permission to update a client."
            )
            return Response(
                {
                    'message': "You are not allowed because you are not a sales member."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )


class ContractViewset(ModelViewSet):
    serializer_class = ContractSerializer

    permission_classes = [IsAuthenticated, IsSalesContact]

    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilter

    def get_permissions(self):
        if self.request.method in ['PUT']:
            return [IsSalesContact()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Contract.objects.all()

        if self.request.user.groups.filter(name='Sales'):
            queryset = queryset.filter(sales_contact=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.has_perm('events.add_contract'):
            contract = request.data.copy()
            contract["sales_contact"] = self.request.user.id
            contract["date_updated"] = date.today()
            serializer = self.get_serializer(data=contract)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.debug("POST contract: OK")
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            logger.debug(
                "POST contract: You are not allowed. Only members of sales team can create a contract. "
            )
            return Response(
                {
                    'message': "You are not allowed. Only members of sales team can create a contract. "
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.has_perm('events.change_client'):
            contract = get_object_or_404(Contract, pk=self.kwargs['pk'])
            self.check_object_permissions(request, contract)
            data = request.data.copy()
            data["date_updated"] = date.today()
            data["sales_contact"] = request.user.id
            serializer = ContractSerializer(contract, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.debug("PUT contract: OK")
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            logger.debug("PUT contract: You are not allowed.")
            return Response(
                {'message': "You are not allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class EventViewset(ModelViewSet):
    serializer_class = EventSerializer

    permission_classes = [
        IsAuthenticated,
        IsSalesContact,
        IsSupportContact,
        HasActiveContract,
    ]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'event_date',
        'client__email',
        'client__last_name',
    ]

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [HasActiveContract()]
        elif self.request.method in ['PUT']:
            if self.request.user.groups.filter(name='Support'):
                return [IsSupportContact()]
            elif self.request.user.groups.filter(name='Sales'):
                return [IsSalesContact()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Event.objects.all()

        if self.request.user.groups.filter(name='Sales'):
            queryset = queryset.filter(client__sales_contact=self.request.user)
            return queryset
        elif self.request.user.groups.filter(name='Support'):
            queryset = queryset.filter(support_contact=self.request.user)
            return queryset
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.has_perm('events.add_event'):
            client_id = request.data["client"]
            client = get_object_or_404(Client, pk=client_id)
            self.check_object_permissions(request, client)

            event = request.data.copy()
            event["date_updated"] = date.today()
            serializer = self.get_serializer(data=event)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.debug("POST event: OK")
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            logger.debug(
                "POST event: You are not allowed. Only members of sales team can create a contract."
            )
            return Response(
                {
                    'message': "You are not allowed. Only members of sales team can create a contract."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.has_perm('events.change_event'):
            data = request.data.copy()
            data["date_updated"] = date.today()
            event = get_object_or_404(Event, pk=self.kwargs['pk'])
            self.check_object_permissions(request, event)
            serializer = EventSerializer(event, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {'message': "You are not allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
