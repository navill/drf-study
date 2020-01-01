from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response

from accounts.api.user.serializers import UserDetailSerializer
from status.api.serializers import StatusInlineUserSerializer
from status.api.views import StatusAPIView
from status.models import Status

User = get_user_model()


class UserDetailAPIView(generics.RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserDetailSerializer
    lookup_field = 'username'

    def get_serializer_context(self):
        return {'request': self.request}


# StatusAPIView 상
# class StatusAPIView(mixins.CreateModelMixin, generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     serializer_class = StatusSerializer
#     passed_id = None
#     search_fields = ('user__username', 'content')
#     ordering_fields = ('user__username', 'timestamp')
#     queryset = Status.objects.all()


class UserStatusAPIView(StatusAPIView):
    serializer_class = StatusInlineUserSerializer

    def get_queryset(self):
        username = self.kwargs.get('username', None)
        if username is None:
            return Status.objects.none()
        return Status.objects.filter(user__username=username)

    # post 오버라이딩을 통해 api/status에서는 post를 작성할 수 있지만,
    # api/user/<username>/status에서는 작성할 수 없음
    def post(self, request, *args, **kwargs):
        return Response({'detail': 'Not allowed here'}, status=400)

# class UserStatusAPIView(StatusAPIView):
#     serializer_class = StatusInlineUserSerializer
#
#     def get_queryset(self):
#         username = self.kwargs.get('username', None)
#         if username is None:
#             return Status.objects.none()
#         return Status.objects.filter(user__username=username)
