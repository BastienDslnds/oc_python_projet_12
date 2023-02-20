from rest_framework import serializers
from .models import Client, Event, Contract


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'mobile',
            'company_name',
            'date_created',
            'date_updated',
            'sales_contact',
        ]


class ClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'mobile',
            'company_name',
            'date_created',
            'date_updated',
            'sales_contact',
            'events',
            'contracts',
        ]

        def get_events(self, instance):

            queryset = instance.events.all()

            serializer = EventSerializer(queryset, many=True)

            return serializer.data

        def get_contracts(self, instance):

            queryset = instance.contracts.all()

            serializer = ContractSerializer(queryset, many=True)

            return serializer.data


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'client',
            'date_created',
            'date_updated',
            'support_contact',
            'event_status',
            'attendees',
            'event_date',
            'notes',
        ]


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            'id',
            'sales_contact',
            'client',
            'date_created',
            'date_updated',
            'signed_status',
            'amount',
            'payment_due',
        ]
