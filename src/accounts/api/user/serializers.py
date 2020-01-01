from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from status.api.serializers import StatusInlineUserSerializer

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    # status_uri = serializers.SerializerMethodField(read_only=True)
    # recent_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'uri', 'status'
        ]

    def get_uri(self, obj):
        request = self.context['request']
        # request 인수를 이용해 full url 출력
        return api_reverse('api-user:detail', kwargs={'username': obj.username}, request=request)
        # return f'/api/users/{obj.id}'

    def get_status(self, obj):
        request = self.context['request']
        limit = 10
        if request:
            limit_query = request.GET.get('limit')
            try:
                limit = int(limit_query)
            except:
                pass
        qs = obj.status_set.all().order_by('-timestamp')
        data = {
            'uri': self.get_uri(obj),
            'last': StatusInlineUserSerializer(qs.first(), context={'request': request}).data,
            'recent_10': StatusInlineUserSerializer(qs[:limit], context={'request': request}, many=True).data,
        }
        return data

    def get_status_uri(self, obj):
        return self.get_uri(obj) + '/status/'

    # def get_recent_status(self, obj):
    #     qs = obj.status_set.all().order_by('-timestamp')[:10]  # 이 유저를 가리키고있는 fk
    #     return StatusInlineUserSerializer(qs, many=True).data
