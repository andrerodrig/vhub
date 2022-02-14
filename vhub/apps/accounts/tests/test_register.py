from django.test import TestCase, Client

from vhub.apps.user.models import User


class TestAccountsViewSets(TestCase):
        
    def test_register(self):
        c = Client()
        response = c.post(
            "/api/accounts/register",
            {
                "email": "test_register@gmail.com",
                "first_name": "teste",
                "last_name": "register",
                "password": "12345",
            },
        )
        self.assertEquals(response.status_code, 201)
    