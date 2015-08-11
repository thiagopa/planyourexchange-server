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

# Customizing display for values
@admin.register(SchoolCourseValue)
class SchoolCourseValueModelAdmin(admin.ModelAdmin):
    list_display = ('course','school','week_price', 'currency',)

    def currency(self,instance):
        return instance.week_price.currency
    
    currency.short_description = 'Currency'
    currency.admin_order_field = 'week_price_currency'

# Utility for not having to select the currency all the time
"""
class SchoolForm(forms.Form):
    enrolment_fee = forms.DecimalField(max_digits=10, decimal_places=2)
    books_fee = forms.DecimalField(max_digits=10, decimal_places=2)
"""    

# Address being edited inside School organized by fieldsets
@admin.register(School)
class SchoolAdmin(ShowIconBaseAdminModel):
    form = DefaultCurrencyForm
    
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

    readonly_fields = ('default_currency',)
    
    def default_currency(self, instance):
        return instance.country.default_currency

    default_currency.short_description = 'Default Currency'
    
# States being edited inside the Country    
class StateInLine(admin.TabularInline):
    model = State

@admin.register(Country)
class CountryAdmin(ShowIconBaseAdminModel):
    inlines = [
        StateInLine
    ]    

# HealthInsurrance with Country List
@admin.register(HealthInsurrance)
class HealthInsuranceModelAdmin(admin.ModelAdmin):
    list_display = ('company_name','country',)

# Grouping different type of quotes
@admin.register(CostOfLiving)
class CostOfLivingModelAdmin(admin.ModelAdmin):
    list_display = ('city','state','country',)
    
    fieldsets = (
        (None, {
            'fields' : ('country','state','city',)
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