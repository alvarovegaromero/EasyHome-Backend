from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView


urlpatterns = [
    path('api/schema/', get_schema_view(title='API Schema'), name='api_schema'),
    path('swagger/', TemplateView.as_view(
        template_name='swagger.html', 
        extra_context={'schema_url':'api_schema'}), 
        name='swagger'),
    path('admin/', admin.site.urls, name='admin'),
    path('api/users/', include('users.urls'), name='users'),
    path('api/groups/', include('groups.urls'), name='groups'),
]
