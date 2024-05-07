from django.urls import path

from .views.groups_view import GroupsAPIView
from .views.create_group_view import GroupCreateAPIView
from .views.group_view import GroupAPIView
from .views.leave_group_view import GroupLeaveAPIView
from .views.join_group_view import GroupJoinAPIView
from .views.get_join_code_view import GroupGenerateCodeAPIView
from .views.get_currencies_view import CurrenciesAPIView
from .views.change_owner_view import GroupChangeOwnerAPIView
from .views.kick_user_view import GroupKickUserAPIView


urlpatterns = [
    path('', GroupsAPIView.as_view(), name='groups'),
    path('currencies', CurrenciesAPIView.as_view(), name='currencies'),
    path('create', GroupCreateAPIView.as_view(), name='create_group'),
    path('join', GroupJoinAPIView.as_view(), name='join_group'), # maybe doesnt follow the restful api standars
    path('<str:group_id>/leave', GroupLeaveAPIView.as_view(), name='leave_group'),
    path('<str:group_id>/generate_code', GroupGenerateCodeAPIView.as_view(), name='generate_code'),
    path('<str:group_id>', GroupAPIView.as_view(), name='group'),
    path('<str:group_id>/kick/<str:user_id>', GroupKickUserAPIView.as_view(), name='kick_user'),
    path('<str:group_id>/change_owner/<str:user_id>', GroupChangeOwnerAPIView.as_view(), name='change_owner'),
]
