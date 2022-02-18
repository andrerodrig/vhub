from django.test import TestCase, Client


class TestDataViewSets(TestCase):
    
    def test_data_list(self):
        c = Client()
        response = c.get("/api/data/")
        self.assertEquals(response.status_code, 404)
        
    