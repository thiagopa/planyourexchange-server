from restserver.models import *
from rest_framework import serializers

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country

class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course

class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = School

# Custom Serializer for weekly price of courses by school
class SchoolCourseValueSerializer(serializers.HyperlinkedModelSerializer):

    week_price = serializers.ReadOnlyField(source='week_price.amount')
    
    class Meta:
        model = SchoolCourseValue
        