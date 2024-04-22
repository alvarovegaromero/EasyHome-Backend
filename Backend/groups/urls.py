from django.urls import path
from .views.groups_view import GroupsAPIView
from .views.create_group_view import GroupCreateAPIView

urlpatterns = [
    path('<str:user_id>/groups', GroupsAPIView.as_view(), name='user_groups'),
    path('create', GroupCreateAPIView.as_view(), name='create_group'),
]
