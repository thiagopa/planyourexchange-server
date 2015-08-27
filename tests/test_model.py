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
from django.test import testcases
from restserver.models import AirFare
from datetime import timedelta

class TestAirFares(testcases.TestCase):
    fixtures = ['restserver_testdata.json']
    
    def test_stops(self):
        airfare = AirFare.objects.get(pk=3)
        stops = airfare.stops()
        self.assertEquals(stops, ['SCL'])
        
        airfare = AirFare.objects.get(pk=1)
        stops = airfare.stops()
        self.assertEquals(stops, ['SCL','AKL'])
        
    def test_total_duration(self):
        airfare = AirFare.objects.get(pk=1)
        total_duration = airfare.total_duration()
        
        self.assertEquals(total_duration,timedelta(days=1,hours=6,minutes=10))