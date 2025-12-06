from django.contrib import admin
from django.urls import path, include
from feedback import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('feedback.urls')),
    path('', include('feedback.frontend_urls')),
    path("debug-env/", views.debug_env),
]
