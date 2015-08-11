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
from djmoney.forms.widgets import CURRENCY_CHOICES
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

    visa_fee = MoneyField(max_digits=10, decimal_places=2)
    default_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)

    class Meta:
        verbose_name_plural = "Countries"

# State in which a city belongs to 
class State(models.Model):
    name = models.CharField(max_length=255)
    abrevation = models.CharField(max_length=5)

# Cities available in each country
class City(AbstractModel): 
    country = models.ForeignKey(Country)
    state = models.ForeignKey(State)
    
    class Meta:
        verbose_name_plural = "Cities"

# Courses that are available to study
class Course(AbstractModel):
    week_duration = models.IntegerField()

# Address used by schools 
class Address(models.Model):
    line = models.CharField(max_length=255)
    suburb = models.CharField(max_length=50)
    zip_code = models.IntegerField()

# Schools that are available    
class School(AbstractModel):
    def default_currency():
        return self.city.country.default_currency
    
    city = models.ForeignKey(City)
    address = models.ForeignKey(Address)
    enrolment_fee = MoneyField(max_digits=10, decimal_places=2)
    books_fee = MoneyField(max_digits=10, decimal_places=2)
    
    
# How much does a course costs in a specific school     
class SchoolCourseValue(models.Model):
    course = models.ForeignKey(Course)
    school = models.ForeignKey(School)
    week_price = MoneyField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return '%s at %s costs %s per week' % (self.course,self.school,self.week_price)
    
    class Meta:
        verbose_name_plural = 'Course Cost per week by School'

# Cost of living per city
class CostOfLiving(models.Model):
    city = models.ForeignKey(City)
    # per meal
    restaurant_average_per_meal = MoneyField(max_digits=10, decimal_places=2)
    # per month
    super_market_average_per_month = MoneyField(max_digits=10, decimal_places=2) 
    
    public_transport_monthly = MoneyField(max_digits=10, decimal_places=2)
    # no shareroom
    rent_average_monthly = MoneyField(max_digits=10, decimal_places=2)
    # utilites
    utilites_average_monthly = MoneyField(max_digits=10, decimal_places=2)

# Health Insurrance Providers per country
class HealthInsurrance(models.Model) :
    country = models.ForeignKey(Country)
    
    company_name = models.CharField(max_length=255)
    company_website = models.CharField(max_length=255)
    
    # per month
    single_price_per_month = MoneyField(max_digits=10, decimal_places=2)
    couple_price_per_month = MoneyField(max_digits=10, decimal_places=2)
    familly_price_per_month = MoneyField(max_digits=10, decimal_places=2)
    
# Generate token for user authentication
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)