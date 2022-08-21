from django.test import TestCase
from rest_framework.test import APIClient


class OrderTests(TestCase):
    first = True
    def setUp(self):
        self.client = APIClient()
        user_data =  [
            {
                    "name": "zhiyuan",
                    "email": "zhiyuan.gao@trilogy.com",
                    "password": "admin"
            },
            {
                    "name": "abcd",
                    "email": "abcd@gmail.com",
                    "password": "password@123"
            }
        ]

        if self.first:
            self.first = False
            sector_data = {
                "name": "Sector",
                "description": "This is 1234"
            }

            stock_data = {
                "name": "Stock 1",
                "price": "100.00",
                "sector": 0,
                "unallocated": 1000,
                "total_volume": 10000000,
            }

            self.client.post('/api/v1/auth/signup/', data = user_data[0], format = "json")
            self.client.post('/api/v1/auth/signup/', data = user_data[1], format = "json")

            response = self.client.post('/api/v1/auth/login/', data = user_data[0], format = "json")
            self.token = ['Token ' + response.data['token']]

            response = self.client.post('/api/v1/auth/login/', data = user_data[1], format = "json")
            self.token.append(('Token ' + response.data['token']))

            response = self.client.post('/api/v1/sectors/', data = sector_data, format = "json", HTTP_AUTHORIZATION = self.token[0])

            response = self.client.post('/api/v1/stocks/', data = stock_data, format = "json", HTTP_AUTHORIZATION = self.token[0])


    def test_order_unauthenticated(self):
        order_data = {
                    "stock": 1,
                    "type": "BUY",
                    "bid_price": "1000.00",
                    "bid_volume": 5
        }
        response = self.client.post('/api/v1/orders/', data = order_data, format = "json")
        self.assertEqual(response.status_code, 401)


    def test_order_invalid_stock(self):
        order_data = {
                    "stock": 200,
                    "type": "BUY",
                    "bid_price": "1000.00",
                    "bid_volume": 5
        }
        response = self.client.post('/api/v1/orders/', data = order_data, format = "json", HTTP_AUTHORIZATION = self.token[0])
        self.assertEqual(response.status_code, 400)
        print('----test_order_invalid_stock----')


    def test_create_buy_order(self):
        order_data = {
                    "stock": 0,
                    "type": "BUY",
                    "bid_price": "100.00",
                    "bid_volume": 500
        }

        response = self.client.post('/api/v1/orders/', data = order_data, format = "json", HTTP_AUTHORIZATION = self.token[0])
        self.assertEqual(response.status_code, 201)


    def test_unaffordable_buy_order(self):
        order_data = {
                    "stock": 0,
                    "type": "BUY",
                    "bid_price": "100000.00",
                    "bid_volume": 500
        }

        response = self.client.post('/api/v1/orders/', data = order_data, format = "json", HTTP_AUTHORIZATION = self.token[0])
        self.assertEqual(response.status_code, 400)


    def test_unaffordable_sell_order(self):
        order_data = {
                    "stock": 1,
                    "type": "SELL",
                    "bid_price": "1000.00",
                    "bid_volume": 50000
        }

        response = self.client.post('/api/v1/orders/', data = order_data, format = "json", HTTP_AUTHORIZATION = self.token[0])
        self.assertEqual(response.status_code, 400)


    def test_get_order(self):
        self.test_create_buy_order()
        response = self.client.get('/api/v1/orders/', HTTP_AUTHORIZATION = self.token[0])
        self.assertEqual(len(response.data),2) 


    def test_match_order(self):
        self.test_create_buy_order()
        response = self.client.post('/api/v1/orders/match/', format = "json", HTTP_AUTHORIZATION = self.token[0])
        self.assertEqual(response.status_code, 404)
