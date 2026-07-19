from django.contrib import admin
from django.urls import path, include
from core.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('triage/', include('triage.urls')),
    path('appointments/', include('appointments.urls')),
    path('', home_view, name='home'),
]