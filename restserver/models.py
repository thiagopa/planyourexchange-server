from django.db import models
from djmoney.models.fields import MoneyField
import moneyed

"""
    @author: Thiago Pagonha
    @version: Jul/2015
"""

# Each model has a name and icon by default
class AbstractModel(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField()

# Countries available to do exchange    
class Country(AbstractModel): pass

# Cities available in each country
class City(AbstractModel): 
    country = models.ForeignKey(Country)

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