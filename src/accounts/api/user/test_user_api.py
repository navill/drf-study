from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase

# Create your tests here.

User = get_user_model()


# api test
class UserTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='cfe', email='jihoon1492@gmail.com')
        user.set_password('test1234')
        user.save()

    def test_created_user_std(self):
        qs = User.objects.filter(username='cfe')
        self.assertEqual(qs.count(), 1)

    def test_created_user_api_fail(self):
        url = api_reverse('api-auth:register')
        data = {
            'username': 'cfe.doe',
            'email': 'cfe.doe@gmail.com',
            'password': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password2'][0], "This field is required.")

    def test_created_user_api_success(self):
        url = api_reverse('api-auth:register')
        data = {
            'username': 'cfe.doe',
            'email': 'cfe.doe@gmail.com',
            'password': 'test1234',
            'password2': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token_len = len(response.data.get('token', 0))
        self.assertGreater(token_len, 0)

    # setUp에 등록된 셋팅을 기준으로 실행되기 때문에 username과 password를 setUp에 일치
    def test_login_user_api(self):
        url = api_reverse('api-auth:login')
        data = {
            'username': 'cfe',
            'password': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token', 0)
        token_len = 0
        if token != 0:
            token_len = len(token)
        self.assertGreater(token_len, 0)

    def test_login_user_api_fail(self):
        url = api_reverse('api-auth:login')
        data = {
            'username': 'cfe2',  # does not exist
            'password': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        token = response.data.get('token', 0)
        token_len = 0
        if token != 0:
            token_len = len(token)
        self.assertEqual(token_len, 0)

    def test_token_login_api(self):
        url = api_reverse('api-auth:login')
        data = {
            'username': 'cfe',
            'password': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token', None)
        # print(token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_token_register_api(self):
        url = api_reverse('api-auth:login')
        data = {
            'username': 'cfe',
            'password': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token', None)
        response2 = self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url2 = api_reverse('api-auth:register')
        data2 = {
            'username': 'cfe.doe',
            'email': 'cfe.doe@gmail.com',
            'password': 'test1234',
            'password2': 'test1234',
        }
        response = self.client.post(url2, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # 403
        # token_len = len(response.data.get('token', 0))
        # self.assertGreater(token_len, 0)
