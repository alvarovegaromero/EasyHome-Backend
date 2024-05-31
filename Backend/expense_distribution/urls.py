from django.urls import path

from .views.expense_detail_view import ExpenseDetailView
from .views.group_expenses_view import GroupExpensesView

urlpatterns = [
    path("<int:group_id>/expenses", GroupExpensesView.as_view(), name="group_expenses"),
    path(
        "<int:group_id>/expenses/<int:expense_id>",
        ExpenseDetailView.as_view(),
        name="expense_detail",
    ),
]
