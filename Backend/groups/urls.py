from django.urls import path
from .views.groups_view import GroupsAPIView

urlpatterns = [
    path('groups', GroupsAPIView.as_view(), name='groups'),
]