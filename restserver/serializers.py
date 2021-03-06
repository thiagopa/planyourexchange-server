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
from restserver.models import *
from restserver.fields import MoneyField
from rest_framework import serializers

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        depth = 1

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        # They're already being rendered inside city object 
        exclude = ('country','state')

# Custom Serializer for weekly price of courses by school
class SchoolCourseValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolCourseValue
        exclude = ('country','state','city')
        depth = 1

# Serializer for find parameters
class SchoolCourseValueFinderSerializer(serializers.Serializer):
    city_id = serializers.IntegerField()
    course_id = serializers.IntegerField(required = False)
    school_id = serializers.IntegerField(required = False)
    
class CostOfLivingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostOfLiving
        # They're already being rendered inside city object 
        exclude = ('country','state')

class HealthInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthInsurance
        depth = 1

class AirTripSerializer(serializers.ModelSerializer):
    origin_airport = serializers.CharField()
    destination_airport = serializers.CharField()

    class Meta:
        model = AirTrip

class AirFareSerializer(serializers.ModelSerializer):
    
    air_trips = AirTripSerializer(many=True)
    
    origin_airport = serializers.CharField()
    destination_airport = serializers.CharField()
    
    price = MoneyField()
    
    class Meta:
        model = AirFare
        depth = 1

class UserLocationSerializer(serializers.Serializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    radius = serializers.FloatField()