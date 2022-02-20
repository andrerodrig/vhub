from pathlib import Path
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.test import override_settings
from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from vhub.apps.user.models import User


class BaseDatasetTest:

    fixtures = [
        "vhub/tests/test_dump_user.json",
        "vhub/tests/test_dump_datasets.json",
    ]

    def _get_csv_file(self, filename: str) -> SimpleUploadedFile:
        file = File(open(filename, "rb"))
        return SimpleUploadedFile(
            name=Path(filename).name,
            content=file.read(),
            content_type="text/csv",
        )


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'tests/media/')
class TestDatasetViewSet(BaseDatasetTest, APITestCase):

    def setUp(self) -> None:
        # Creating the test user
        self.user = User.objects.get(pk=1)
        self.token = Token.objects.create(user=self.user)
        self.client.login(
            email="test_user@gmail.com", password="12345"
        )
        self.client.force_authenticate(user=self.user, token=self.token.key)

    def tearDown(self) -> None:
        self.user.delete()

    def test_get_list_of_datasets(self):
        response = self.client.get("/api/datasets/")
        self.assertEquals(response.status_code, 200)

    def test_create_a_dataset(self):
        csv_file = self._get_csv_file("vhub/tests/dataset_test.csv")
        data = {
            "name": "test_dataset",
            "file": csv_file,
        }
        response = self.client.post(
            path="/api/datasets/",
            data=data,
            files=csv_file,
        )
        self.assertEquals(response.status_code, 201)


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'tests/media/')
class TestDatasetDetailViewSet(BaseDatasetTest, APITestCase):

    def setUp(self) -> None:
        # Creating the test user
        self.user = User.objects.get(pk=1)
        self.token = Token.objects.create(user=self.user)
        self.client.login(
            email="test_user@gmail.com", password="12345"
        )
        self.client.force_authenticate(user=self.user, token=self.token.key)

    def tearDown(self) -> None:
        self.user.delete()

    def test_retrieve_a_dataset(self):
        response = self.client.get("/api/datasets/1")
        self.assertEquals(response.status_code, 200)

    def test_update_a_dataset(self):
        data = {
            "name": "test_dataset2",
        }
        response = self.client.put(
            path="/api/datasets/1",
            data=data,
        )
        self.assertEquals(response.status_code, 202)

    def test_does_not_update_readonly_field(self):
        dataset1 = self.client.get("/api/datasets/1").data
        file_old = dataset1.get("file")
        csv_file = self._get_csv_file("vhub/tests/dataset_test.csv")
        data = {
            "name": "test_dataset2",
            "file": csv_file,
        }
        response = self.client.put(
            path="/api/datasets/1",
            data=data,
            files=csv_file,
        )
        self.assertEquals(response.data.get("file"), file_old)

    def test_delete_a_dataset(self):
        response = self.client.delete(path="/api/datasets/1")
        self.assertEquals(response.status_code, 204)
