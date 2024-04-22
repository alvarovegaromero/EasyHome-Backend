from django.urls import path
from .views.groups_view import GroupsAPIView
from .views.create_group_view import GroupCreateAPIView
from .views.group_view import GroupAPIView
from .views.leave_group_view import GroupLeaveAPIView

urlpatterns = [
    path('<str:user_id>/groups', GroupsAPIView.as_view(), name='groups'),
    path('create', GroupCreateAPIView.as_view(), name='create_group'),
    path('<str:group_id>', GroupAPIView.as_view(), name='group'),
    path('<str:group_id>/leave', GroupLeaveAPIView.as_view(), name='leave_group'),
]
