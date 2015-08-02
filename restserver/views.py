from rest_framework import viewsets, status
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
    
    # Load School values according to given city, course or school 
    @list_route(methods=['post'])
    def find(self, request):
        serializer = SchoolCourseValueFinderSerializer(data=request.data)
        if serializer.is_valid() :
            
            # Creating filters dynamically and stripping out nulls if needed
            filters = {'school__city_id' : serializer.data.get('city_id'),
                       'school__id' : serializer.data.get('school_id'),
                       'course__id' : serializer.data.get('course_id')
            }
            filters = dict(filter(lambda (k,v): v is not None, filters.items()))
            
            queryset = SchoolCourseValue.objects.filter(**filters)
            # If queryset is empty tell it is not found
            if not queryset.exists() :
                return Response(status=status.HTTP_404_NOT_FOUND)
            # serialize the result
            serializer = SchoolCourseValueSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
            
    
