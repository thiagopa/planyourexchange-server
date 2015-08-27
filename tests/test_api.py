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
from rest_framework import status
from nose.tools import raises
from restserver.models import Country
from test_utils import BaseTest

class CountriesTest(BaseTest):
    """
        Test all api calls related to Countries 
    """
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
        self.generic_list('/api/countries/','No countries listed at all :(')
    
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
        self.assertEquals(country.visa_fee, 1850.0)
    
    def test_list_cities(self):
        self.generic_list('/api/countries/1/cities/','No cities found for Australia')

    def test_list_healthinsurances(self):
        self.generic_list('/api/countries/1/healthinsurances/','No Health Insurances found for Australia')


class CitiesTest(BaseTest):
    """
        Test api only relevant calls to Cities
    """
    def test_list_courses(self):
        self.generic_list('/api/cities/2/courses/','No Courses being taught in Sydney')
        
    def test_list_schools(self):
        self.generic_list('/api/cities/2/schools/','No Schools found in Sydney')
        
    def test_list_cost_of_living(self):
        response = self.client.get('/api/cities/2/costofliving/')
        
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertEquals(response.data['city'],2)
        
class SchoolCourseValueTest(BaseTest):
    """
        Test finder filter for prices based on the school and the course
    """
    def test_city_required(self):
        data = {
            'course_id' : 2 
        }
        
        response = self.client.post('/api/schoolcoursevalue/find/', data)
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_school_city(self):
        data = {
            'city_id' : 2,
            'school_id': 4
        }
        self.generic_school_course_city(data)

    def test_course_city(self):
        data = {
            'city_id' : 2,
            'course_id': 3
        }
        self.generic_school_course_city(data)
    
    def generic_school_course_city(self,data):
        """
            Takes the parameters to the call and the expected object of return
        """
        response = self.client.post('/api/schoolcoursevalue/find/', data)
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0, 'No values found for school or course in this city')

class AirFareTest(BaseTest):
    def test_gru_syd(self):
        self.generic_list('/api/airfares/?origins=GRU&destination=SYD','No airfares for GRU to SYD')

    def test_multiple_origins(self):
        self.generic_list('/api/airfares/?origins=GRU,OOS&destination=SYD','No airfares for multiple destinations to SYD')
        
    def test_airports_near_paris(self):
        data = {
            'latitude' : 48.84,
            'longitude' : 2.367,
            'radius' : 40 
        }
        response = self.client.post('/api/airports/',data)
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertEquals(response.data , ["ORY","TNF","LBG","CDG"])
        
