from rest_framework.permissions import BasePermission
from .models import Contract, Client, Event


class IsSalesContact(BasePermission):
    """Permission to check if the authenticated user is
    the sales contact of the client or the contract."""

    message = "You're not allowed because you're not the sales contact of the client."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        print("TEST")
        if isinstance(obj, Contract) or isinstance(obj, Client):
            if obj.sales_contact == request.user:
                return True
            return False
        elif isinstance(obj, Event):
            if obj.client.sales_contact == request.user:
                return True
            return False


class IsSupportContact(BasePermission):
    """Permission to check if the authenticated user is
    the support contact of the client or the contract."""

    message = "You're not allowed because you're not the support contact."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if obj.support_contact == request.user:
            return True
        return False
