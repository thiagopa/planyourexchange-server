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
from django.contrib import admin
from django import forms
from models import *
from moneyed import CURRENCIES
import autocomplete_light

# Base Model to show real image of Icons intead of urls in forms
@admin.register(Course)
class ShowIconBaseAdminModel(admin.ModelAdmin):
    readonly_fields = ('icon_display',)
    
    def icon_display(self, instance):
        return u'<img src="%s" />' % instance.icon.url

    icon_display.short_description = 'Icon Display Image'
    icon_display.allow_tags = True

# Show City with full hierarchy display
@admin.register(City)
class CityModelAdmin(ShowIconBaseAdminModel):
    list_display = ('name','state','country',)

# Default Currency
class DefaultCurrencyAdminModel(admin.ModelAdmin):
    readonly_fields = ('default_currency',)
    
    def default_currency(self,instance):
        return CURRENCIES[instance.country.default_currency].name
    
    default_currency.description = 'Default Currency'

# Customizing display for values
@admin.register(SchoolCourseValue)
class SchoolCourseValueModelAdmin(DefaultCurrencyAdminModel):
    list_display = ('course','school','week_price', 'default_currency',)

    fieldsets = (
        ('Course', {
            'fields' : ('course',)
        }),
        ('School',{
            'fields' : ('country','state','city','school',)
        }),
        ('Price',{
            'fields' : ('default_currency','week_price',)
        }),
    )

# Address being edited inside School organized by fieldsets
@admin.register(School)
class SchoolAdmin(DefaultCurrencyAdminModel,ShowIconBaseAdminModel):
    
    readonly_fields = ('icon_display','default_currency')
    
    fieldsets = (
        (None, {
            'fields' : ('name','icon','icon_display',)
        }),
        ('Address',{
            'fields' : ('address_line','suburb','zip_code','country','state','city',)
        }),
        ('Fees',{
            'fields' : ('default_currency', 'enrolment_fee','books_fee',)
        }),
    )
    
# States being edited inside the Country    
class StateInLine(admin.TabularInline):
    model = State

@admin.register(Country)
class CountryAdmin(ShowIconBaseAdminModel):
    inlines = [
        StateInLine
    ]    

# HealthInsurrance with Country List
@admin.register(HealthInsurance)
class HealthInsuranceModelAdmin(DefaultCurrencyAdminModel,ShowIconBaseAdminModel):
    readonly_fields = ('icon_display','default_currency')
    
    list_display = ('name','country',)
    
    fieldsets = (
        (None, {
            'fields' : ('name','icon','icon_display','country','website')
        }),
        ('Prices', {
            'fields' : ('default_currency','single_price_per_month','couple_price_per_month','familly_price_per_month')
        }),
    )

# Grouping different type of quotes
@admin.register(CostOfLiving)
class CostOfLivingModelAdmin(DefaultCurrencyAdminModel):

    list_display = ('city','state','country',)
    
    fieldsets = (
        (None, {
            'fields' : ('country','state','city','default_currency')
        }),
        ('Food',{
            'fields' : ('restaurant_average_per_meal','super_market_average_per_month',)
        }),
        ('Transport',{
            'fields' : ('public_transport_monthly',)
        }),
        ('Housing',{
            'fields' : ('rent_average_monthly','utilites_average_monthly',)
        }),

    )

@admin.register(AirFare)
class AirFareModelAdmin(admin.ModelAdmin):
    list_display = ('price','origin','destination','total_duration','stops')

"""
Register the auto complete and create a new model form for AirTrips
"""
from restserver.auto_complete import AirPortAutoComplete
autocomplete_light.register(AirPortAutoComplete)

class AirTripModelForm(forms.ModelForm):
    origin = forms.CharField(widget=autocomplete_light.TextWidget('AirPortAutoComplete'))
    destination = forms.CharField(widget=autocomplete_light.TextWidget('AirPortAutoComplete'))
    
    class Meta:
        model = AirTrip
        fields = '__all__'

@admin.register(AirTrip)
class AirTripAdmin(admin.ModelAdmin):
    form = AirTripModelForm