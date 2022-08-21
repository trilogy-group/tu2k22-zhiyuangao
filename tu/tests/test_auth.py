from django.test import TestCase
from rest_framework.test import APIClient

class UserRegisterTests(TestCase):
    token = ''
    def setUp(self):
        self.client = APIClient()


    def test_signup(self):
        user_data =  {
                    "name": "zhiyuan",
                    "email": "zhiyuan.gao@trilogy.com",
                    "password": "admin"
            }

        response = self.client.post('/api/v1/auth/signup/', data=user_data, format="json")
        assert(response.status_code == 201)



    def test_login(self):
        user_data = {
                    "name": "zhiyuan",
                    "email": "zhiyuan@trilogy.com",
                    "password": "admin"
        }

        response = self.client.post('/api/v1/auth/signup/', data=user_data, format="json")
        assert(response.status_code == 201)

        response = self.client.post('/api/v1/auth/login/', data=user_data, format="json")
        self.token = response.data['token']
        assert(response.status_code == 200)


    def test_profile_fail(self):
        response = self.client.get('/api/v1/auth/profile/', data={}, format="json", HTTP_AUTHORIZATION = "Token " + self.token)
        self.assertEqual(response.status_code, 404)

    def test_logout_success(self):
        user_data = {
                    "name": "zhiyuan_test_logout_success",
                    "email": "zhiyuan.gao_test_logout_success@trilogy.com",
                    "password": "admin"
        }

        response = self.client.post('/api/v1/auth/signup/', data=user_data, format="json")
        assert(response.status_code == 201)

        response = self.client.post('/api/v1/auth/login/', data=user_data, format="json")
        assert(response.status_code == 200)

        token = response.data["token"]

        response = self.client.post('/api/v1/auth/logout/', HTTP_AUTHORIZATION = "Token " + token)
        assert(response.status_code == 204)


    def test_logout_fail(self):
        user_data = {
                    "name": "zhiyuan_test_logout_fail",
                    "email": "zhiyuan.gao_test_logout_fail@trilogy.com",
                    "password": "admin"
        }

        response = self.client.post('/api/v1/auth/signup/', data=user_data, format="json")
        assert(response.status_code == 201)

        response = self.client.post('/api/v1/auth/login/', data=user_data, format="json")
        assert(response.status_code == 200)

        token = "123wrongtoken"

        response = self.client.post('/api/v1/auth/logout/', HTTP_AUTHORIZATION = "Token " + token)
        assert(response.status_code == 401)


    def test_no_email(self):
        body = {
            "password": "admin"
        }

        response = self.client.post('/api/v1/auth/signup/', data=body, format="json")
        assert(response.status_code==400)

        response = self.client.post('/api/v1/auth/signin/', data=body, format="json")
        assert(response.status_code==404)
