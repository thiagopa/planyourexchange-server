from rest_framework import viewsets
from restserver.serializers import *
from restserver.models import *

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    
class SchoolCourseValueViewSet(viewsets.ModelViewSet):
    queryset = SchoolCourseValue.objects.all()
    serializer_class = SchoolCourseValueSerializer