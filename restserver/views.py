from rest_framework import viewsets
from restserver.serializers import *
from restserver.models import *
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    
    # Extra method for loading cities according to the parent country
    @detail_route()
    def cities(self,request,pk=None):
        queryset = City.objects.filter(country=self.get_object())
        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data)
    
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    
    # Load courses according to the city
    @detail_route()
    def courses(self,request,pk=None):
        queryset = SchoolCourseValue.objects.filter(school__city=self.get_object())
        # Transfer all courses from relationship to serializer
        serializer = CourseSerializer([scv.course for scv in queryset], many=True)
        return Response(serializer.data)
        
    
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    
class SchoolCourseValueViewSet(viewsets.ModelViewSet):
    queryset = SchoolCourseValue.objects.all()
    serializer_class = SchoolCourseValueSerializer