from django.urls import path

from .views.shared_board_view import SharedBoardView

urlpatterns = [
    path('<str:group_id>', SharedBoardView.as_view(), name='shared_board'),
]
