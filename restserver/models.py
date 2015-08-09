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
from django.db import models
from djmoney.models.fields import MoneyField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import moneyed

# Each model has a name and icon by default
class AbstractModel(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='icons')
    
    def __str__(self):
        return self.name

# Countries available to do exchange    
class Country(AbstractModel):
    class Meta:
        verbose_name_plural = "Countries"

# Cities available in each country
class City(AbstractModel): 
    country = models.ForeignKey(Country)
    
    class Meta:
        verbose_name_plural = "Cities"

# Courses that are available to study
class Course(AbstractModel):
    week_duration = models.IntegerField()

# Schools that are available    
class School(AbstractModel):
    city = models.ForeignKey(City)
    
# How much does a course costs in a specific school     
class SchoolCourseValue(models.Model):
    course = models.ForeignKey(Course)
    school = models.ForeignKey(School)
    week_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    
    def __str__(self):
        return '%s at %s costs %s per week' % (self.course,self.school,self.week_price)
    
    class Meta:
        verbose_name_plural = 'Course Cost per week by School'

# Generate token for user authentication
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)