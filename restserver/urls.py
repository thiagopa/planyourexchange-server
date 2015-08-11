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
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from rest_framework import routers
from restserver import views
from rest_framework.authtoken.views import obtain_auth_token

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'countries',views.CountryViewSet)
router.register(r'cities',views.CityViewSet)
router.register(r'courses',views.CourseViewSet)
router.register(r'schools',views.SchoolViewSet)
router.register(r'schoolcoursevalue',views.SchoolCourseValueViewSet)

urlpatterns = [
    # Static web page
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    # rest api
    url(r'^api/', include(router.urls)),
    url(r'^api/token-auth/', obtain_auth_token),
    # django admin
    url(r'^admin/', include(admin.site.urls)),
    # django admin chaining combos
    url(r'^chaining/', include('smart_selects.urls')), 
]
