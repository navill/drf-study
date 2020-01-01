from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

# from .utils import jwt_response_payload_handler
from accounts.api.permissions import ANonPermissionOnly
from accounts.api.serializers import UserRegisterSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class AuthAPIView(APIView):
    authentication_classes = []
    permission_classes = [ANonPermissionOnly]

    def post(self, request, *args, **kwargs):
        # 인증(로그인 전 시점) - anonymous user
        # print(request.user)
        if request.user.is_authenticated:
            return Response({'detail': 'You are already authenticated'}, status=400)
        data = request.data
        username = data.get('username')
        password = data.get('password')
        qs = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).distinct()
        if qs.exists():
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                # 인증 된 시점 - jh
                print(user)
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                return Response(response)
        return Response({'detail': 'Invalid credentials'}, status=401)


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [ANonPermissionOnly]

    def ge_serializer_context(self):
        return {'request': self.request}  # -> serializer에 request 전달

# 위와 동일한 코드
# class RegisterAPIView(APIView):
#     authentication_classes = []
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({'detail': 'You are already registered and authenticated'}, status=400)
#         data = request.data
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')
#         password2 = data.get('password')
#
#         qs = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username))
#         if password != password2:
#             return Response({'password': 'Password must match'}, status=401)
#         if qs.exists():
#             return Response({'detail': 'This user already exists'}, status=401)
#         else:
#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             # token을 보내지 않을 경우 아래 주석처리
#             # payload = jwt_payload_handler(user)
#             # token = jwt_encode_handler(payload)
#             # response = jwt_response_payload_handler(token, user, request=request)
#             # return Response(response, status=201)
#             return Response({'detail':'Thank you for registering. Please verify your email'}, status=201)
#         # return Response({'detail': 'Invalid credentials'}, status=401)
