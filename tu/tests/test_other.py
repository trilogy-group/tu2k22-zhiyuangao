from django.test import TestCase
from rest_framework.test import APIClient

class OtherTests(TestCase):

    def setUp(self):
        self.client = APIClient()


    def test_signup(self):
        user_data =  {"logFiles": ["https://codejudge-question-artifacts.s3.ap-south-1.amazonaws.com/q-2476/log1.txt","https://codejudge-question-artifacts.s3.ap-south-1.amazonaws.com/q-2476/log2.txt"],"parallelFileProcessingCount": 15}

        response = self.client.post('/api/v1/process-logs/', data=user_data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_log(self):
        response = self.client.get('/log/', data={}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_open(self):
        response = self.client.post('/api/v1/market/open', data={}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_log(self):
        response = self.client.post('/github/login', data={}, format="json")
        self.assertEqual(response.status_code, 200)


