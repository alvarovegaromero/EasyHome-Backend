from django.urls import path

from .views.group_expenses_view import GroupExpensesView

urlpatterns = [
    path("<int:group_id>/expenses", GroupExpensesView.as_view(), name="group_expenses"),
]
