from restserver.models import *
from rest_framework import serializers

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country

class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    
    class Meta:
        model = City

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School

# Custom Serializer for weekly price of courses by school
class SchoolCourseValueSerializer(serializers.ModelSerializer):

    week_price = serializers.ReadOnlyField(source='week_price.amount')
    
    class Meta:
        model = SchoolCourseValue
        