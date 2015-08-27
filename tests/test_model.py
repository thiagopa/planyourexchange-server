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

class TestAirFares(testcases.TestCase):
    fixtures = ['restserver_testdata.json']
    
    def setUp(self):
        self.airfare = AirFare.objects.get(pk=3) 
    
    def test_AirFare_stops(self):
        stops = self.airfare.stops()
        self.assertEquals(stops, ['SCL'])