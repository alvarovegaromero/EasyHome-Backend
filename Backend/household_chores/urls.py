from django.urls import path

from .views.assignable_task_update_view import AssignableTaskUpdateAPIView
from .views.assignable_tasks_in_range_view import AssignableTasksInRangeAPIView
from .views.assignable_tasks_today_view import AssignableTasksTodayAPIView
from .views.task_list_create_view import TaskListCreateAPIView
from .views.task_retrieve_update_delete_view import TaskRetrieveUpdateDeleteAPIView

urlpatterns = [
    path("<str:group_id>/tasks", TaskListCreateAPIView.as_view(), name="tasks"),
    path(
        "<str:group_id>/tasks/<str:task_id>", TaskRetrieveUpdateDeleteAPIView.as_view(), name="task"
    ),
    path(
        "<str:group_id>/tasks/assign/today",
        AssignableTasksTodayAPIView.as_view(),
        name="assign_task",
    ),
    path(
        "<str:group_id>/tasks/assign/<str:assignable_task_id>",
        AssignableTaskUpdateAPIView.as_view(),
        name="complete_assignable_task",
    ),
    path(
        "<str:group_id>/tasks/assign/",
        AssignableTasksInRangeAPIView.as_view(),
        name="assignable_task_range",
    ),
]
