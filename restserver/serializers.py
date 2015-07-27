from restserver.models import *
from rest_framework import serializers
from djmoney.models.fields import MoneyField

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

# Custom Serializer for Money
class MoneyFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyField
        fields = ('amount','currency')

# Custom Serializer for values of courses by school
class SchoolCourseValueSerializer(serializers.HyperlinkedModelSerializer):
    
    week_price = MoneyFieldSerializer() 
    
    class Meta:
        model = SchoolCourseValue
        fields = ('url','course','school','week_price')
