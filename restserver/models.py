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
from djmoney.forms.widgets import CURRENCY_CHOICES
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from smart_selects.db_fields import ChainedForeignKey
from djmoney.models.fields import MoneyField
from datetime import timedelta
from sets import Set
from restserver import geo_airports

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
    visa_fee = models.DecimalField(max_digits=10, decimal_places=2)
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

class CityAirport(AbstractModel):
    """
        Airports that are available in the City
    """
    airport = models.CharField(max_length=3)

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

    airport = models.ManyToManyField(CityAirport)

    class Meta:
        verbose_name_plural = "Cities"

class Course(AbstractModel):
    """
        Courses that are available to study
    """
    week_duration = models.IntegerField()
    is_flexible = models.BooleanField(default=False)


class School(AbstractModel):
    """
        Schools that are available
    """
    # Chaining the city selection to whichever country and state is selected
    country = models.ForeignKey(Country)
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country")
    city = ChainedForeignKey(City, chained_field="state", chained_model_field="state")
    # fees
    enrolment_fee = models.DecimalField(max_digits=10, decimal_places=2)
    books_fee = models.DecimalField(max_digits=10, decimal_places=2)
    # address
    address_line = models.CharField(max_length=255)
    suburb = models.CharField(max_length=50)
    postal_code = models.CharfField(max_length=255)

# How much does a course costs in a specific school
class SchoolCourseValue(models.Model):
    course = models.ForeignKey(Course)

    # Chaining the school selection all the way up to country,state and city
    country = models.ForeignKey(Country)
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country")
    city = ChainedForeignKey(City, chained_field="state", chained_model_field="state")
    school = ChainedForeignKey(School, chained_field="city", chained_model_field="city")

    week_price = models.DecimalField(max_digits=10, decimal_places=2)

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
    restaurant_average_per_meal = models.DecimalField(verbose_name="Average meal in Restaurant",max_digits=10, decimal_places=2)
    # per month
    super_market_average_per_month = models.DecimalField(verbose_name="Average Supermarket per Month", max_digits=10, decimal_places=2)

    public_transport_monthly = models.DecimalField(verbose_name="Monthly Public Transport ticket",max_digits=10, decimal_places=2)
    # no shareroom
    rent_average_monthly = models.DecimalField(verbose_name="Average Rent per Month",max_digits=10, decimal_places=2)
    # utilites
    utilites_average_monthly = models.DecimalField(verbose_name="Average Utilites per Month",max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Costs of Living"

class HealthInsurance(AbstractModel) :
    """
        Health Insurance Providers per country
    """
    country = models.ForeignKey(Country)
    website = models.URLField()

    # per month
    single_price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    couple_price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    familly_price_per_month = models.DecimalField(max_digits=10, decimal_places=2)

def airport_name(key):
    return geo_airports.get(key,'name')

class AirHelper:
    """
    Returns the full name for airports
    """
    @property
    def origin_airport(self):
        return airport_name(self.origin)

    @property
    def destination_airport(self):
        return airport_name(self.destination)

class AirTrip(models.Model,AirHelper):
    """
        Represents a trip that would ultimetily lead to final destination
    """
    operated_by = models.CharField(max_length=255)

    trip_sequence = models.IntegerField(default=1)

    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)

    flight_duration = models.DurationField()

    airport_layover = models.DurationField(blank=True, default=timedelta())

    def __str__(self):
        return '%s to %s operated by %s' % (self.origin,self.destination,self.operated_by)

    class Meta:
        ordering = ['trip_sequence']

class AirFare(models.Model,AirHelper):
    """
        AirFare object represents a "cached" air fare
    """
    date = models.DateField()

    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)

    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

    air_trips = models.ManyToManyField(AirTrip)

    def save(self, *args, **kwargs):
        """
            Overriding origin and desination to uppercase
        """
        self.origin = self.origin.upper()
        self.destination = self.destination.upper()
        super(AirFare,self).save( *args, **kwargs)

    def total_duration(self):
        """
            Total duration from all trips
            Sums all flight and airport connection durations
        """
        trips_duration = [(lambda x,y : x + y)(t.flight_duration,t.airport_layover) for t in self.air_trips.all()]
        return sum(trips_duration,timedelta())

    def stops(self):
        """
            Should only show intermediate airports, excluding origin and destination
            First append origin and destination to a list if they're not the origin and destination already
            Last remove duplicates
        """
        s = Set()
        [(lambda x,y : [s.add(x), s.add(y)]) (t.origin,t.destination) for t in self.air_trips.all()]
        s.remove(self.origin)
        s.remove(self.destination)
        return list(s)

# Generate token for user authentication
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
