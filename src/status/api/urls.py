from django.urls import path

# from .views import StatusListSearchAPIView
from .views import StatusAPIView, StatusDetailAPIView

app_name = 'api-status'
urlpatterns = [
    path('', StatusAPIView.as_view()),
    # path('create/', StatusCreateAPIView.as_view()),
    path('<int:id>/', StatusDetailAPIView.as_view(), name='detail'),
    # path('<id>/update/', StatusUpdateAPIView.as_view()),
    # path('<id>/delete/', StatusDeleteAPIView.as_view()),
]
