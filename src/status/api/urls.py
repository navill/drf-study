from django.urls import path

# from .views import StatusListSearchAPIView
from .views import StatusAPIView

urlpatterns = [
    path('', StatusAPIView.as_view()),
    # path('create/', StatusCreateAPIView.as_view()),
    # path('<int:id>/', StatusDetailAPIView.as_view()),
    # path('<id>/update/', StatusUpdateAPIView.as_view()),
    # path('<id>/delete/', StatusDeleteAPIView.as_view()),
]
