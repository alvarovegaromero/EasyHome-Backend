from django.shortcuts import get_object_or_404
from groups.models import Group, UserGroup
from rest_framework.permissions import BasePermission


class IsGroupMember(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs["group_id"]
        group = get_object_or_404(Group, id=group_id)
        return UserGroup.is_member(request.user, group)
