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
from rest_framework import viewsets, status
from restserver.serializers import *
from restserver.models import *
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    
    @detail_route()
    def cities(self,request,pk=None):
        """
            Load Cities according to the parent country
        """
        return self.generic_data_load(City,CitySerializer)
        
    @detail_route()
    def healthinsurrances(self,request,pk=None):
        """
        Load Health Insurances per Country
        """
        return self.generic_data_load(HealthInsurrance,HealthInsurranceSerializer)
    
    def generic_data_load(self,model,serializer_class):
        queryset = model.objects.filter(country=self.get_object())
        serializer = serializer_class(queryset,many=True)
        return Response(serializer.data)
    
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    
    @detail_route()
    def courses(self,request,pk=None):
        return self.generic_data_load(CourseSerializer,lambda scv: scv.course)
    
    @detail_route()
    def schools(self,request,pk=None):
        return self.generic_data_load(SchoolSerializer,lambda scv: scv.school)
    
    def generic_data_load(self,serializer_class,query_object):
        """
             Transfer all schools/courses from relationship to serializer
             Because it comes duplicated, use set to only show unique results
        """
        queryset = SchoolCourseValue.objects.filter(school__city=self.get_object())
        serializer = serializer_class(set([query_object(scv) for scv in queryset]), many=True)
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
            
    
