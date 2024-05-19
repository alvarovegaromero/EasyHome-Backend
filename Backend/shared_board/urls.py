from django.urls import path

from .views.shared_board_view import SharedBoard

urlpatterns = [
    path('', SharedBoard.as_view(), name='groups'),
]
