# from django.views.generic import View
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins

from status.api.serializers import StatusSerializer
from status.models import Status


# # CreateModelMixin -- POST Method
# # UpdateModelMixin -- PUT Method
# # DestroyModelMxin -- DELETE Method
class StatusAPIView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    # queryset = Status.objects.all()
    serializer_class = StatusSerializer

    # get-> retrieve -> get_object -> get_queryset
    def get_queryset(self):
        request = self.request
        qs = Status.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def get_object(self):
        request = self.request
        passed_id = request.GET.get('id', None)
        queryset = self.get_queryset()
        obj = None
        if passed_id is not None:
            obj = get_object_or_404(queryset, id=passed_id)
            self.check_object_permissions(request, obj)
        return obj

    # HTTP method
    def get(self, request, *args, **kwargs):
        passed_id = request.GET.get('id', None)
        # request.body
        # request.data
        if passed_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
#
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
