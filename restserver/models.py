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

class AbstractModel(models.Model):
    """
        Each model has a name and icon by default
    """
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='icons')
    
    def __str__(self):
        return self.name

class Country(AbstractModel):
    """
        Countries available to do exchange 
    """
    visa_fee = MoneyField(max_digits=10, decimal_places=2)
    default_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)

    class Meta:
        verbose_name_plural = "Countries"

class State(models.Model):
    """
        State in which a city belongs to 
    """
    country = models.ForeignKey(Country) 
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=5)
    
    def __str__(self):
        return self.abbreviation


class City(AbstractModel):
    """
        Cities available in each country
    """ 
    country = models.ForeignKey(Country)
    state = ChainedForeignKey(State,
        chained_field="country",
        chained_model_field="country", 
        show_all=False, 
        auto_choose=True)
    
    class Meta:
        verbose_name_plural = "Cities"

class Course(AbstractModel):
    """
        Courses that are available to study
    """
    week_duration = models.IntegerField()

class School(AbstractModel):
    """
        Schools that are available    
    """
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

# How much does a course costs in a specific school     
class SchoolCourseValue(models.Model):
    course = models.ForeignKey(Course)
    school = models.ForeignKey(School)
    week_price = MoneyField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return '%s at %s costs %s per week' % (self.course,self.school,self.week_price)
    
    class Meta:
        verbose_name_plural = 'Course Cost per week by School'

class CostOfLiving(models.Model):
    """
        Cost of living per city
    """
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

class HealthInsurance(models.Model) :
    """
        Health Insurance Providers per country
    """
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

# Used to save all currencies with the default country
@receiver(pre_save)
def default_currency(sender, instance, *args, **kwargs):
    default_currency = None
    
    if hasattr(instance,'country_id'):
        default_currency = instance.country.default_currency
    elif hasattr(instance,'default_currency'):
        default_currency = instance.default_currency
    
    if default_currency:
        for attr in dir(instance):
            if attr.endswith('currency'):
                setattr(instance,attr,default_currency)
