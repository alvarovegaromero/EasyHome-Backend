from django.urls import path

from .views.assignable_task_update_view import AssignableTaskUpdateAPIView
from .views.assignable_tasks_in_range_view import AssignableTasksInRangeAPIView
from .views.assignable_tasks_today_view import AssignableTasksTodayAPIView
from .views.check_assignable_tasks_active_view import CheckAssignableTasksActiveAPIView
from .views.start_assignable_task_view import StartAssignableTasksAPIView
from .views.task_list_create_view import TaskListCreateAPIView
from .views.task_update_delete_view import TaskUpdateDeleteAPIView

urlpatterns = [
    path("<int:group_id>/tasks", TaskListCreateAPIView.as_view(), name="tasks"),
    path("<int:group_id>/tasks/<int:task_id>", TaskUpdateDeleteAPIView.as_view(), name="task"),
    path(
        "<int:group_id>/tasks/start_assignable",
        StartAssignableTasksAPIView.as_view(),
        name="start_assignable_tasks",
    ),
    path(
        "<int:group_id>/tasks/assign/active",
        CheckAssignableTasksActiveAPIView.as_view(),
        name="check_assignable_tasks_active",
    ),
    path(
        "<int:group_id>/tasks/assign/today",
        AssignableTasksTodayAPIView.as_view(),
        name="assign_task",
    ),
    path(
        "<int:group_id>/tasks/assign/<int:assignable_task_id>",
        AssignableTaskUpdateAPIView.as_view(),
        name="complete_assignable_task",
    ),
    path(
        "<int:group_id>/tasks/assign/range",
        AssignableTasksInRangeAPIView.as_view(),
        name="assignable_task_range",
    ),
]
