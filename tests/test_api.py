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
from nose.tools import raises
from restserver.models import Country
import json

class AuthenticatedTest(APITestCase):
    """
        Creates and Authenticate a test user using the api
        Loads default fixture data for other objects
    """
    fixtures = ['restserver_testdata.json']
    
    def setUp(self):
        self.superuser = User.objects.create_superuser('testuser', 'test@planyourexchange.com', 'testpassword')
        response = self.client.post('/api/token-auth/', {'username' : 'testuser', 'password' : 'testpassword' })
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + json.loads(response.content)['token'])
        
class CountriesTest(AuthenticatedTest):
    
    def test_create_country(self):
        with open('tests/test_icon.png') as test_icon:
            data = {
                    'name' : 'Australia',
                    'icon' : test_icon,
                    'visa_fee' : 550.0,
                    'default_currency' : 'AUD'
            } 
        
            response = self.client.post('/api/countries/', data, 'multipart')
            
            self.assertEquals(response.status_code,status.HTTP_201_CREATED)

    def test_get_country(self):
        response = self.client.get('/api/countries/1/')
        
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertEquals(response.data['id'],1)
    
    def test_list_countries(self):
        response = self.client.get('/api/countries/')
        
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0, 'No countries listed')
    
    @raises(Country.DoesNotExist)        
    def test_delete_country(self):
        response = self.client.delete('/api/countries/1/')
        self.assertEquals(response.status_code,status.HTTP_204_NO_CONTENT)
        
        country = Country.objects.get(pk=1)
        
    def test_update_visa_fee(self):
        data = {
            'visa_fee' : 1850.0
        }
        
        response = self.client.patch('/api/countries/1/', data)
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        
        country = Country.objects.get(pk=1)
        self.assertEquals(country.visa_fee.amount, 1850.0)
    
    def test_list_cities(self):
        response = self.client.get('/api/countries/1/cities/')
        
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0, 'No cities listed')
        
            