from django.urls import path

from .views.task_list_create_view import TaskListCreateAPIView
from .views.task_retrieve_update_delete_view import TaskRetrieveUpdateDeleteAPIView

urlpatterns = [
    path("<str:group_id>/tasks", TaskListCreateAPIView.as_view(), name="tasks"),
    path(
        "<str:group_id>/tasks/<str:task_id>", TaskRetrieveUpdateDeleteAPIView.as_view(), name="task"
    ),
]
