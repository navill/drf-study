from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='jh2', email='jihoon1492@gmail.com')
        user.set_password('gkdl1493')
        user.save()

    def test_created_user(self):
        qs = User.objects.filter(username='jh2')
        self.assertEqual(qs.count(), 1)
