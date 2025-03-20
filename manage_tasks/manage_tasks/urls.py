from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from tasks.views import test_endpoint
from tasks.views import manage_task

urlpatterns = [
    path('test/', test_endpoint, name='test_endpoint'),  
    path('admin/', admin.site.urls),
    path('', manage_task, name='manage_task'),  # Set the main view for managing tasks
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)