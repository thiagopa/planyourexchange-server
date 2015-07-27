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

class SchoolCourseValueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SchoolCourseValue