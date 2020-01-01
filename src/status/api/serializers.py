from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from accounts.api.serializers import UserPublicSerializer
from status.models import Status

"""
class CustomSerializer(serializers.Serializer):
    content = serializers.CharField()
    email = serializers.EmailField()
    
data = {'email': 'naver@naver.com', 'content':'please delete me'}
create_obj_serializer = CustomSerializer(data=data)
if create_obj_serializer.is_valid():
    data = create_obj_serializer.data
    print(data)
"""


class StatusSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    user = UserPublicSerializer(read_only=True)
    # user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Status
        fields = [
            'uri',
            'id',
            'user',
            'content',
            'image',
        ]
        read_only_fields = ['user']

    def get_uri(self, obj):
        request = self.context['request']
        return api_reverse('api-status:detail', kwargs={'id': obj.id}, request=request)

    # def get_user(self, obj):
    #     request = self.context['request']
    #     user = obj.user
    #     return UserPublicSerializer(user, read_only=True, context={'request': request}).data

    """
    def validate_<fieldname>(self, value):
        validation...
        return value
   """

    # Field level validation
    # def validate_content(self, value):
    #     if len(value) > 10000:
    #         raise serializers.ValidationError("This is way too long.")
    #     return value

    # Serializer level validation
    def validate(self, data):
        content = data.get('content', None)
        if content == '':
            content = None
        image = data.get('image', None)
        if image is None and content is None:
            raise serializers.ValidationError('Content or image is required')
        return data


class StatusInlineUserSerializer(StatusSerializer):
    # uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Status
        fields = [
            'uri',
            'id',
            'content',
            'image',
        ]

# class StatusInlineUserSerializer(StatusSerializer):
#     uri = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = Status
#         fields = [
#             'uri',
#             'id',
#             'content',
#             'image',
#         ]
#
#     def get_uri(self, obj):
#         request = self.context['request']
#         return api_reverse('api-status:detail', kwargs={'id': obj.id}, request=request)
