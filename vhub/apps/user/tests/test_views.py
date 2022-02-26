from django.test import override_settings
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from vhub.apps.user.models import User


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'tests/media/')
class TestCommonUserViewSet(APITestCase):

    fixtures = [
        "vhub/tests/test_dump_user.json",
    ]

    def setUp(self) -> None:
        # Creating the test user
        self.user = User.objects.get(pk=1)
        self.token = Token.objects.create(user=self.user)
        self.client.login(
            email="test_user@gmail.com", password="12345"
        )
        self.client.force_authenticate(user=self.user, token=self.token.key)

    def test_cannot_access_user_list(self):
        response = self.client.get("/api/user/")
        self.assertEquals(response.status_code, 403)

    def test_cannot_update_user(self):
        data = {
            "email": "superuser@gmail.com",
            "name": "dummy",
            "is_superuser": False,
        }
        response = self.client.post(
            "/api/user/2",
            data=data
        )
        self.assertEquals(response.status_code, 403)

    def test_cannot_delete_user(self):
        response = self.client.delete("/api/user/2")
        self.assertEquals(response.status_code, 403)


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'tests/media/')
class TestSuperUserViewSets(APITestCase):

    fixtures = [
        "vhub/tests/test_dump_user.json",
    ]

    def setUp(self) -> None:
        # Creating the test user
        self.user = User.objects.get(pk=2)
        self.token = Token.objects.create(user=self.user)
        self.client.login(
            email="superuser@gmail.com", password="12345"
        )
        self.client.force_authenticate(user=self.user, token=self.token.key)

    def test_can_access_user_list(self):
        response = self.client.get("/api/user/")
        self.assertEquals(response.status_code, 200)

    def test_can_update_user(self):
        data = {
            "email": "test_user@gmail.com",
            "first_name": "dummy",
            "last_name": "user",
        }
        response = self.client.put(
            path="/api/user/1",
            data=data
        )
        self.assertEquals(response.status_code, 202)

    def test_can_delete_user(self):
        response = self.client.delete("/api/user/1")
        self.assertEquals(response.status_code, 204)
