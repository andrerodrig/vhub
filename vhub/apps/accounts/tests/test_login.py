from django.test import TestCase, Client

from vhub.apps.user.models import User


class TestAccountsViewSets(TestCase):
        
    def test_login(self):
        c = Client()
        _ = c.post(
            "/api/accounts/register",
            {
                "email": "test_login@gmail.com",
                "first_name": "teste",
                "last_name": "login",
                "password": "12345",
            },
        )
        login_response = c.post(
            "/api/accounts/login",
            {"email": "test_login@gmail.com", "password": "12345"}
        )
        self.assertEquals(login_response.status_code, 200)
