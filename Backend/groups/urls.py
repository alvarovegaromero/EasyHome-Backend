from django.urls import path
from .views.groups_view import GroupsAPIView

urlpatterns = [
    path('<str:user_id>/groups', GroupsAPIView.as_view(), name='user_groups'),
]