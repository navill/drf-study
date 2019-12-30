# from django.views.generic import View
import json

from rest_framework import generics, mixins, permissions
from rest_framework.authentication import SessionAuthentication

from status.api.serializers import StatusSerializer
from status.models import Status


# # CreateModelMixin -- POST Method
# # UpdateModelMixin -- PUT Method
# # DestroyModelMxin -- DELETE Method
def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid


class StatusDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class StatusAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView):
    # 허가(permission)에 따라 어떻게 동작할 것인가?
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # 어떻게 인증을 할 것인지??
    # authentication_classes = [SessionAuthentication]  # Oauth, JWT
    # queryset = Status.objects.all()
    serializer_class = StatusSerializer
    passed_id = None

    # get-> retrieve -> get_object -> get_queryset
    def get_queryset(self):
        request = self.request
        qs = Status.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class StatusAPIView(
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     generics.ListAPIView):
#     permission_classes = []
#     authentication_classes = []
#     # queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#     passed_id = None
#
#     # get-> retrieve -> get_object -> get_queryset
#     def get_queryset(self):
#         request = self.request
#         qs = Status.objects.all()
#         query = request.GET.get('q')
#         if query is not None:
#             qs = qs.filter(content__icontains=query)
#         return qs
#
#     def get_object(self):
#         request = self.request
#         passed_id = request.GET.get('id', None) or self.passed_id
#         queryset = self.get_queryset()
#         obj = None
#         if passed_id is not None:
#             obj = get_object_or_404(queryset, id=passed_id)
#             self.check_object_permissions(request, obj)
#         return obj
#
#     # HTTP method
#     def get(self, request, *args, **kwargs):
#         url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         body_ = request.body
#         if is_json(body_):
#             json_data = json.loads(body_)
#         new_passed_id = json_data.get('id', None)
#         # print(request.body)  # b'{"id": 5}'
#         # request.data
#         passed_id = url_passed_id or new_passed_id or None
#         self.passed_id = passed_id
#         if passed_id is not None:
#             return self.retrieve(request, *args, **kwargs)
#         return super().get(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         body_ = request.body
#         if is_json(body_):
#             json_data = json.loads(body_)
#         new_passed_id = json_data.get('id', None)
#         request_id = request.data.get('id')
#         passed_id = url_passed_id or new_passed_id or request_id or None
#         self.passed_id = passed_id
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         body_ = request.body
#         if is_json(body_):
#             json_data = json.loads(body_)
#         new_passed_id = json_data.get('id', None)
#         # print(request.body)  # b'{"id": 5}'
#         # request.data
#         passed_id = url_passed_id or new_passed_id or None
#         self.passed_id = passed_id
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         body_ = request.body
#         if is_json(body_):
#             json_data = json.loads(body_)
#         new_passed_id = json_data.get('id', None)
#         # print(request.body)  # b'{"id": 5}'
#         # request.data
#         passed_id = url_passed_id or new_passed_id or None
#         self.passed_id = passed_id
#         return self.destroy(request, *args, **kwargs)

# class StatusListSearchAPIView(APIView):  # Create & List
#     permission_classes = []
#     authentication_classes = []
#
#     def get(self, request, foramt=None):
#         qs = Status.objects.all()
#         serializer = StatusSerializer(qs, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         qs = Status.objects.all()
#         serializer = StatusSerializer(qs, many=True)
#         return Response(serializer.data)
#
#

#
#     # def perform_create(self, serializer):
#     #     serializer.save(user=self.request.user)
#
#
# class StatusDetailAPIView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.RetrieveAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#
#     # # url field 지정 pk -> id
#     # lookup_field = 'id'  # id, slug, ....
#
#     # def get_object(self):
#     #     kwargs = self.kwargs
#     #     kw_id = kwargs.get('id')
#     #     return Status.objects.get(id=kw_id)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#
#
# class StatusUpdateAPIView(generics.UpdateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#     # url field 지정 pk -> id
#     lookup_field = 'id'  # id, slug, ....
#
#
# class StatusDeleteAPIView(generics.DestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#     # url field 지정 pk -> id
#     lookup_field = 'id'  # id, slug, ....
