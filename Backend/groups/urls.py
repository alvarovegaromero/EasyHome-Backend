from django.urls import path
from .views.groups_view import GroupsAPIView
from .views.create_group_view import GroupCreateAPIView
from .views.group_view import GroupAPIView

urlpatterns = [
    path('<str:user_id>/groups', GroupsAPIView.as_view(), name='groups'),
    path('create', GroupCreateAPIView.as_view(), name='create_group'),
    path('<str:user_id>', GroupAPIView.as_view(), name='group'),
]
