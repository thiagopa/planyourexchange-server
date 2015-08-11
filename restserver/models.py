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
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from smart_selects.db_fields import ChainedForeignKey 
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
    country = models.ForeignKey(Country) 
    name = models.CharField(max_length=255)
    abreviation = models.CharField(max_length=5)
    
    def __str__(self):
        return self.abreviation


# Cities available in each country
class City(AbstractModel): 
    country = models.ForeignKey(Country)
    state = ChainedForeignKey(State,
        chained_field="country",
        chained_model_field="country", 
        show_all=False, 
        auto_choose=True)
    
    class Meta:
        verbose_name_plural = "Cities"

# Courses that are available to study
class Course(AbstractModel):
    week_duration = models.IntegerField()

# Schools that are available    
class School(AbstractModel):
    
    # Chaining the city selection to whichever country and state is selected
    country = models.ForeignKey(Country)
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country")
    city = ChainedForeignKey(City, chained_field="state", chained_model_field="state")
    # fees
    enrolment_fee = MoneyField(max_digits=10, decimal_places=2)
    books_fee = MoneyField(max_digits=10, decimal_places=2)
    # address
    address_line = models.CharField(max_length=255)
    suburb = models.CharField(max_length=50)
    zip_code = models.IntegerField()

# Save default value for currencies
@receiver(pre_save, sender=School)
def save_default_currency(sender, instance, **kwargs):
    instance.enrolment_fee.default_currency = instance.country.default_currency
    instance.books_fee.default_currency = instance.country.default_currency
    
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
    # Chaining the city selection to whichever country and state is selected
    country = models.ForeignKey(Country)
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country")
    city = ChainedForeignKey(City, chained_field="state", chained_model_field="state")
    
    # per meal
    restaurant_average_per_meal = MoneyField(verbose_name="Average meal in Restaurant",max_digits=10, decimal_places=2)
    # per month
    super_market_average_per_month = MoneyField(verbose_name="Average Supermarket per Month", max_digits=10, decimal_places=2) 
    
    public_transport_monthly = MoneyField(verbose_name="Monthly Public Transport ticket",max_digits=10, decimal_places=2)
    # no shareroom
    rent_average_monthly = MoneyField(verbose_name="Average Rent per Month",max_digits=10, decimal_places=2)
    # utilites
    utilites_average_monthly = MoneyField(verbose_name="Average Utilites per Month",max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name_plural = "Costs of Living"


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
