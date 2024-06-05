from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from ...groups.models import Group


class IsGroupOwner(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs["group_id"]
        group = get_object_or_404(Group, id=group_id)
        return group.owner == request.user
