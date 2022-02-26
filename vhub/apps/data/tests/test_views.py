from pathlib import Path
from django.conf import settings
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from vhub.apps.user.models import User

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'tests/media/')
class BaseDataTest(APITestCase):
    """Base test class for Data"""

    fixtures = [
        "vhub/tests/test_dump_user.json",
        "vhub/tests/test_dump_datasets.json",
    ]

    def setUp(self) -> None:
        # Creating the test user
        self.user = User.objects.get(pk=1)
        self.token = Token.objects.create(user=self.user)
        self.client.login(
            email="test_user@gmail.com", password="12345"
        )
        self.client.force_authenticate(user=self.user, token=self.token.key)
        csv_file = self._get_csv_file("vhub/tests/dataset_test.csv")
        data = {
            "name": "test_dataset",
            "file": csv_file,
        }
        _ = self.client.post(
            path="/api/datasets/",
            data=data,
            files=csv_file,
        )

    def tearDown(self) -> None:
        self.user.delete()

    def _get_csv_file(self, filename: str) -> SimpleUploadedFile:
        file = File(open(filename, "rb"))
        return SimpleUploadedFile(
            name=Path(filename).name,
            content=file.read(),
            content_type="text/csv",
        )


class TestDataViewSets(BaseDataTest):
    """Test classe for listing data from a dataset."""

    def test_wrong_endpoint_data_list_results_404(self):
        response = self.client.get("/api/data/")
        self.assertEquals(response.status_code, 404)

    def test_correct_endpoint_data_list_results_200(self):
        response = self.client.get("/api/data/datasets/1")
        self.assertEquals(response.status_code, 200)


class TestDataDetailViewSets(BaseDataTest):
    """
    Test classe for retrieving, creating, updating and deleting
    data from a dataset.
    """
    def test_retrieve_a_data(self):
        response = self.client.get("/api/data/1")
        self.assertEquals(response.status_code, 200)

    def test_update_a_data_with_success(self):
        data = {
            "solved": True,
        }
        response = self.client.put(
            path="/api/data/1",
            data=data,
        )
        self.assertEquals(response.status_code, 202)

    def test_does_not_update_readonly_field(self):
        data1 = self.client.get("/api/data/1").data
        data = {
            "hostname": "renamed",
            "ip_address": "1.2.2.2.1",
            "title": "renamed_title",
            "severity": "low",
            "cvss": "1000",
            "publication_date": "2350-01-01"
        }
        response = self.client.put(
            path="/api/data/1",
            data=data
        )
        for key in data:
            self.assertEquals(response.data.get(key), data1.get(key))

    def test_delete_a_data(self):
        response = self.client.delete(path="/api/data/1")
        self.assertEquals(response.status_code, 204)
