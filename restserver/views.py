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
from rest_framework import viewsets, status, generics
from restserver.serializers import *
from restserver.models import *
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
import django_filters
from restserver import geo_airports

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (DjangoModelPermissions,)
    
    @detail_route()
    def cities(self,request,pk=None):
        """
            Load Cities according to the parent country
        """
        return self.generic_data_load(City,CitySerializer)
        
    @detail_route()
    def healthinsurances(self,request,pk=None):
        """
        Load Health Insurances per Country
        """
        return self.generic_data_load(HealthInsurance,HealthInsuranceSerializer)
    
    def generic_data_load(self,model,serializer_class):
        queryset = model.objects.filter(country=self.get_object())
        serializer = serializer_class(queryset,many=True)
        return Response(serializer.data)
    
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (DjangoModelPermissions,)
    
    @detail_route()
    def courses(self,request,pk=None):
        return self.generic_data_load(CourseSerializer,lambda scv: scv.course)
    
    @detail_route()
    def schools(self,request,pk=None):
        return self.generic_data_load(SchoolSerializer,lambda scv: scv.school)
    
    @detail_route()
    def costofliving(self,request,pk=None):
        queryset = CostOfLiving.objects.filter(city=self.get_object())
        if queryset.exists():
            serializer = CostOfLivingSerializer(queryset.first())
            return Response(serializer.data)
        else :
            return Response('No data could be found',
                            status=status.HTTP_404_NOT_FOUND)
    
    def generic_data_load(self,serializer_class,query_object):
        """
             Transfer all schools/courses from relationship to serializer
             Because it comes duplicated, use set to only show unique results
        """
        queryset = SchoolCourseValue.objects.filter(school__city=self.get_object())
        if queryset.exists():
            serializer = serializer_class(set([query_object(scv) for scv in queryset]), many=True)
            return Response(serializer.data)
        else :
            return Response('No data could be found',
                            status=status.HTTP_404_NOT_FOUND)

        
class SchoolCourseValueViewSet(viewsets.ModelViewSet):
    queryset = SchoolCourseValue.objects.all()
    serializer_class = SchoolCourseValueSerializer
    permission_classes = (DjangoModelPermissions,)
    
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

class AirFareListView(generics.ListAPIView):
    """
        AirFare view list, search multiple origins and one destination
    """
    serializer_class = AirFareSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        origins = self.request.query_params.get('origins', None)
        destination = self.request.query_params.get('destination',None)
        
        if origins is not None and destination is not None:
            return AirFare.objects.filter(origin__in=origins.split(','),destination=destination)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def nearby_airports(request):
    """
        Uses GeoBases component to identify which are the nearest airports for the given radius
        Allows anyone who is authenticated because this view doesn't access database
    """
    location = UserLocationSerializer(data=request.data)
    if location.is_valid() :
        airports = geo_airports.findNearPoint((location.data['latitude'], location.data['longitude']), location.data['radius'])
        return Response([k for _,k in airports])
    else :
        return Response(location.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        
