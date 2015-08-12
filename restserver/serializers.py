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
    visa_fee = MoneyField()
    
    class Meta:
        model = Country

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State

class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    state = StateSerializer(read_only=True)
    
    class Meta:
        model = City

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course

class SchoolSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    
    enrolment_fee = MoneyField()
    books_fee = MoneyField()
    
    class Meta:
        model = School
        # They're already being rendered inside city object 
        exclude = ('country','state')

# Custom Serializer for weekly price of courses by school
class SchoolCourseValueSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    week_price = MoneyField()
    
    class Meta:
        model = SchoolCourseValue

# Serializer for find parameters
class SchoolCourseValueFinderSerializer(serializers.Serializer):
    city_id = serializers.IntegerField()
    course_id = serializers.IntegerField(required = False)
    school_id = serializers.IntegerField(required = False)
    
class CostOfLivingSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    restaurant_average_per_meal = MoneyField()
    super_market_average_per_month = MoneyField() 
    public_transport_monthly = MoneyField()
    rent_average_monthly = MoneyField()
    utilites_average_monthly = MoneyField()
    
    class Meta:
        model = CostOfLiving
        # They're already being rendered inside city object 
        exclude = ('country','state')

class HealthInsuranceSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    
    single_price_per_month = MoneyField()
    couple_price_per_month = MoneyField()
    familly_price_per_month = MoneyField()

    class Meta:
        model = HealthInsurance