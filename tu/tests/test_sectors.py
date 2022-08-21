from django.test import TestCase

from rest_framework.test import APIClient


class SectorTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        user_data =  {
                    "name": "zhiyuan_sector",
                    "email": "zhiyuan_sector@trilogy.com",
                    "password": "admin"
        }

        self.client.post('/api/v1/auth/signup/', data = user_data, format = "json")
        response = self.client.post('/api/v1/auth/login/', data = user_data, format = "json")
        self.token = 'Token ' + response.data['token']


    def test_create_sector(self):
        sector_data = {"name": "Sector1", "description": "Zhiyuan sector1"}
        response = self.client.post('/api/v1/sectors/', data = sector_data, format = "json", HTTP_AUTHORIZATION = self.token)
        self.assertEqual(response.status_code, 201)


    def test_create_sector_unauthenticated(self):
        sector_data = {"name": "Sector2", "description": "unauthenticated sector. no token"}
        response = self.client.post('/api/v1/sectors/', data = sector_data, format = "json")
        self.assertEqual(response.status_code, 401)


    def test_get_sectors(self):
        response = self.client.get('/api/v1/sectors/')
        self.assertEqual(len(response.data), 2)
        print('----test_get_sectors----')


    def test_get_sector(self):
        response = self.client.get('/api/v1/sectors/0/')
        self.assertEqual(response.status_code, 200)
        print('----test_get_sector----')


    def test_patch_sector_id(self):
        new_sector_data = {"name": "patch Sector!!", "description": "This is patched sector"}

        response = self.client.patch('/api/v1/sectors/0/', data=new_sector_data, HTTP_AUTHORIZATION = self.token)
        assert(response != None)


    def test_patch_sector_id_no_auth(self):
        #self.test_create_sector()
        new_sector_data = {"name": "New Sector Name", "description": "This is first sector"}
        response = self.client.patch('/api/v1/sectors/1/', data = new_sector_data)

        self.assertEqual(response.status_code, 401)


    """
    def test_patch_sector_id_no_id(self):
        self.test_create_sector()
        new_sector_data = {"name": "New Sector Name", "description": "This is first sector"}
        response = self.client.patch('/api/v1/sectors/', data = new_sector_data)
        self.assertEqual(response.status_code, 401)


    def test_patch_sector_invalid_id(self):
        self.test_create_sector()
        new_sector_data = {"name": "New Sector Name", "description": "This is first sector"}
        response = self.client.patch('/api/v1/sectors/1234455334/', data = new_sector_data)
        self.assertEqual(response.status_code, 401)
    """
