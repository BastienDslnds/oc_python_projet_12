import django_filters
from .models import Contract


class ContractFilter(django_filters.FilterSet):

    last_name = django_filters.CharFilter(
        field_name='client__last_name', lookup_expr='icontains'
    )
    email = django_filters.CharFilter(
        field_name='client__email', lookup_expr='icontains'
    )

    class Meta:
        model = Contract
        fields = ['date_created', 'amount', 'client']
