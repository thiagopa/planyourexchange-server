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
    city = CitySerializer(read_only=True)
    
    class Meta:
        model = School

# Custom Serializer for weekly price of courses by school
class SchoolCourseValueSerializer(serializers.ModelSerializer):

    week_price = serializers.ReadOnlyField(source='week_price.amount')
    
    class Meta:
        model = SchoolCourseValue

# Serializer for find parameters
class SchoolCourseValueFinderSerializer(serializers.Serializer):
    city_id = serializers.IntegerField()
    course_id = serializers.IntegerField(required = False)
    school_id = serializers.IntegerField(required = False)