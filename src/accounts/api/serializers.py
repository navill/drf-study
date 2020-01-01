import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from accounts.api.utils import expire_delta

User = get_user_model()


# class UserDetailSerializer(serializers.ModelSerializer):
#     uri = serializers.SerializerMethodField(read_only=True)
#     status_list = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = User
#         fields = [
#             'id', 'username', 'uri'
#         ]
#
#     def get_uri(self, obj):
#         return f'/api/users/{obj.id}'
#
#     def get_status_list(self, obj):
#         return obj


class UserPublicSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'uri'
        ]

    def get_uri(self, obj):
        request = self.context['request']
        return api_reverse('api-user:detail', kwargs={'username': obj.username}, request=request)


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    success_message = serializers.SerializerMethodField(read_only=True)

    # token_response = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'token',
            # 'token_response',
            'expires',
            'success_message',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    # def get_token_response(self, obj):
    #     payload = jwt_payload_handler(obj)
    #     token = jwt_encode_handler(payload)
    #     context = self.context
    #     response = jwt_response_payload_handler(token, obj, request=context['request'])
    #     return response

    def get_success_message(self, obj):
        return 'Thank you for registering'

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError('User with this email already exists')
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError('User with this email already exists')
        return value

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, data):
        pw = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError('Passwords must match')
        return data

    def create(self, validated_data):
        user_obj = User(username=validated_data['username'], email=validated_data['email'])
        user_obj.set_password(validated_data['password'])
        # 가입 후 email 유효성 검사 이후 True
        user_obj.is_active = False
        user_obj.save()
        return user_obj
