from django.test import TestCase
from rest_framework.test import APIClient


class StockTests(TestCase):
    first = True
    def setUp(self):
        self.client = APIClient()
        user_data=  {
                    "name": "zhiyuan",
                    "email": "zhiyuan.gao@trilogy.com",
                    "password": "admin"
        }
        if self.first:
            first = False
            self.client.post('/api/v1/auth/signup/', data = user_data, format = "json")
            response = self.client.post('/api/v1/auth/login/', data = user_data, format = "json")
            self.token = 'Token ' + response.data['token']

            sector_data = {"name": "First Sector", "description": "This is the first sector"}
            response = self.client.post('/api/v1/sectors/', data = sector_data, format = "json", HTTP_AUTHORIZATION = self.token)

    def test_create_stocks_unauthenticated(self):
        stock_data = {
                    "name": "Stock 1",
                    "price": "100.00",
                    "sector": 0,
                    "unallocated": 0,
                    "total_volume": 0
        }
        response = self.client.post('/api/v1/stocks/', data = stock_data, format = "json")
        self.assertEqual(response.status_code, 401)


    def test_create_stocks_missing_field(self):
        stock_data = {
                    "name": "Stock 1",
                    "price": "100.00",
                    "sector": 0,
                    "unallocated": 0,
        }
        response = self.client.post('/api/v1/stocks/', data = stock_data, format = "json", HTTP_AUTHORIZATION = self.token)
        self.assertEqual(response.status_code, 400)


    def test_create_stocks(self):
        stock_data = {
                    "name": "Stock 1",
                    "price": "100.00",
                    "sector": 1,
                    "unallocated": 0,
                    "total_volume": 0
        }
        response = self.client.post('/api/v1/stocks/', data = stock_data, format = "json", HTTP_AUTHORIZATION = self.token)
        self.assertEqual(response.status_code, 201)


    def test_get_stocks_by_id(self):
        #self.test_create_stocks()
        response = self.client.get('/api/v1/stocks/0/')

        self.assertEqual(response.status_code,200)


    def test_get_stocks(self):
        #self.test_create_stocks()
        response = self.client.get('/api/v1/stocks/')

        self.assertEqual(response.data[0]['id'],0)


