from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from accounts.api.views import AuthAPIView, RegisterAPIView

app_name = 'api-auth'

urlpatterns = [
    path('', AuthAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('jwt/', obtain_jwt_token),
    path('jwt/refresh/', refresh_jwt_token),
]
