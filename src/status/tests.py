# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase

from status.models import Status

User = get_user_model()


class StatusTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='jh', email='jihoon1493@gmail.com')
        user.set_password('gkdl1493')
        user.save()

    def test_creating_status(self):
        user = User.objects.get(username='jh')
        obj = Status.objects.create(user=user, content='test content')
        self.assertEqual(obj.id, 1)
        qs = Status.objects.all()
        self.assertEqual(qs.count(), 1)
