"""
    Copyright (C) 2015, Thiago Pagonha,
    Plan Your Exchange, easy exchange to fit your budget
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Affero General Public License for more details.
    
    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
import json

class AuthenticatedTest(APITestCase):
    """
        Creates and Authenticate a test user using the api
    """
    def setUp(self):
        self.superuser = User.objects.create_superuser('testuser', 'test@planyourexchange.com', 'testpassword')
        response = self.client.post('/api/token-auth/', {'username' : 'testuser', 'password' : 'testpassword' })
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + json.loads(response.content)['token'])
        
class CountriesTest(AuthenticatedTest):
    
    def test_create_country(self):
        with open('restserver/test_icon.png') as test_icon:
            data = {
                    'name' : 'Australia',
                    'icon' : test_icon,
                    'visa_fee' : 550.0,
                    'default_currency' : 'AUD'
            } 
        
            response = self.client.post('/api/countries/', data, 'multipart')
        
            print response
        
            self.assertEquals(response.status_code,status.HTTP_200_OK)
    
    def test_list_countries(self):
        response = self.client.get('/api/countries/')
        
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertTrue(response.content, 'No countries listed')

# Using the standard RequestFactory API
#factory = APIRequestFactory()
#request = factory.get('/countries/')