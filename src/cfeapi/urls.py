from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/status/', include('status.api.urls')),
    path('api/auth/', include('accounts.api.urls')),
    path('api/user/', include('accounts.api.user.urls')),
]
