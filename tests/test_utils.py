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
from inmemorystorage import InMemoryStorage
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

class TestStorage(InMemoryStorage):
    """
        Addressing NotImplementedException Issues
    """
    def url(self, name):
        return name

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

class GenericTests:
    def generic_list(self,url):
        """
            Verify calls that need to return a list of objects
        """
        response = self.client.get(url,message)
        
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0, message)
        
