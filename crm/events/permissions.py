from rest_framework.permissions import BasePermission


class IsSalesContact(BasePermission):
    """Permission to check if the authenticated user is
    the sales contact of the client or the contract."""

    message = "You're not allowed because you're not the sales contact of the client."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if type(obj) == "<class 'crm.events.models.Contract'>":
            if obj.sales_contact == request.user:
                return True
            return False
        elif type(obj) == "<class 'crm.events.models.Event'>":
            if obj.client.sales_contact == request.user:
                return True
            return False


class IsSupportContact(BasePermission):
    """Permission to check if the authenticated user is
    the support contact of the client or the contract."""

    message = "You're not allowed because you're not the author."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if obj.support_contact == request.user:
            return True
        return False
