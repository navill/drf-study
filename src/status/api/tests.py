import os
import shutil  # shell utility
import tempfile

from PIL import Image  # Pillow
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

# from rest_framework_jwt.settings import api_settings
# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from status.models import Status

User = get_user_model()


# api test
class StatusTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', email='jihoon1492@gmail.com')
        user.set_password('test1234')
        user.save()
        Status.objects.create(user=user, content='hello!')
        # print(status_obj)

    def test_statuses(self):
        self.assertEqual(Status.objects.count(), 1)

    # acquire token
    def status_user_token(self):
        auth_url = api_reverse('api-auth:login')
        auth_data = {
            'username': 'testuser',
            'password': 'test1234',
        }
        auth_response = self.client.post(auth_url, auth_data, format='json')
        token = auth_response.data.get('token', 0)
        # set jwt token
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    # create item
    def create_item(self):
        self.status_user_token()
        url = api_reverse('api-status:list')
        data = {
            'content': 'come cool test content'
        }
        response = self.client.post(url, data, format='json')  # item 2
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), 2)
        return response.data

    # empty create item
    def empty_create_item(self):
        self.status_user_token()
        url = api_reverse('api-status:list')
        data = {
            'content': None,
            'image': None
        }
        response = self.client.post(url, data, format='json')  # item 2
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data

    # create with image - create
    def test_status_create_with_image_and_no_content(self):
        self.status_user_token()
        url = api_reverse('api-status:list')
        # (w, h) = (800, 1280)
        # (255, 255, 255)
        image_item = Image.new('RGB', (800, 1280), (0, 125, 175))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image_item.save(tmp_file, format='JPEG')
        with open(tmp_file.name, 'rb') as file_obj:
            data = {
                'content': '',
                'image': file_obj,
            }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Status.objects.count(), 2)

        # test에 사용된 이미지 파일 삭제
        temp_img_dir = os.path.join(settings.MEDIA_ROOT, 'status', 'testuser')
        if os.path.exists(temp_img_dir):
            shutil.rmtree(temp_img_dir)

    # create with image - create
    def test_status_create_with_image(self):
        self.status_user_token()
        url = api_reverse('api-status:list')
        # (w, h) = (800, 1280)
        # (255, 255, 255)
        image_item = Image.new('RGB', (800, 1280), (0, 125, 175))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image_item.save(tmp_file, format='JPEG')
        with open(tmp_file.name, 'rb') as file_obj:
            data = {
                'content': 'come cool test content with image',
                'image': file_obj,
            }
            response = self.client.post(url, data, format='multipart')
            # print(response.data)

            img_data = response.data.get('image')
            self.assertNotEqual(img_data, None)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Status.objects.count(), 2)

        # test에 사용된 이미지 파일 삭제
        temp_img_dir = os.path.join(settings.MEDIA_ROOT, 'status', 'testuser')
        if os.path.exists(temp_img_dir):
            shutil.rmtree(temp_img_dir)

    # get - retrieve
    def test_status_retrieve(self):
        data = self.create_item()
        # print(response.data)
        data_id = data.get('id')
        rud_url = api_reverse('api-status:detail', kwargs={'id': data_id})

        get_response = self.client.get(rud_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    # put - update
    def test_status_update(self):
        data = self.create_item()
        # print(response.data)
        data_id = data.get('id')
        rud_url = api_reverse('api-status:detail', kwargs={'id': data_id})
        rud_data = {
            'content': 'another new content'
        }

        put_response = self.client.put(rud_url, rud_data, format='json')
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        rud_response_data = put_response.data
        self.assertEqual(rud_response_data['content'], rud_data['content'])

    # delete - destroy
    def test_status_delete(self):
        data = self.create_item()
        # print(response.data)
        data_id = data.get('id')
        rud_url = api_reverse('api-status:detail', kwargs={'id': data_id})

        delete_response = self.client.delete(rud_url, format='json')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        # not found
        response = self.client.get(rud_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_status_without_token_create(self):
        url = api_reverse('api-status:list')
        data = {
            'content': 'some cool test content without token'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_other_user_permission_api(self):
        data = self.create_item()
        data_id = data.get('id')
        user = User.objects.create(username='othertestuser')
        payload = jwt_payload_handler(user)
        print(payload)
        token = jwt_encode_handler(payload)
        print(token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        rud_url = api_reverse('api-status:detail', kwargs={'id': data_id})
        rud_data = {
            'content': 'permission test'
        }
        get_ = self.client.get(rud_url, format='json')
        put_ = self.client.put(rud_url, rud_data, format='json')
        delete_ = self.client.delete(rud_url, format='json')
        self.assertEqual(get_.status_code, status.HTTP_200_OK)
        self.assertEqual(put_.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_.status_code, status.HTTP_403_FORBIDDEN)
