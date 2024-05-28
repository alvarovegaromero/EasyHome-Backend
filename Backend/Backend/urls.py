from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path("api/schema/", get_schema_view(title="API Schema"), name="api_schema"),
    path(
        "swagger/",
        TemplateView.as_view(
            template_name="swagger.html", extra_context={"schema_url": "api_schema"}
        ),
        name="swagger",
    ),
    path("admin/", admin.site.urls, name="admin"),
    path("api/users/", include("users.urls"), name="users"),
    path("api/groups/", include("groups.urls"), name="groups"),
    path("api/shared_board/", include("shared_board.urls"), name="shared_board"),
    path(
        "api/expense_distribution/",
        include("expense_distribution.urls"),
        name="expense_distribution",
    ),
]
