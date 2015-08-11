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
from models import *

# Base Model to show real image of Icons intead of urls in forms
class ShowIconBaseAdminModel(admin.ModelAdmin):
    readonly_fields = ('icon_display',)
    
    def icon_display(self, instance):
        return u'<img src="%s" />' % instance.icon.url

    icon_display.short_description = 'Icon Display Image'
    icon_display.allow_tags = True

# Customizing display for values
class SchoolCourseValueModelAdmin(admin.ModelAdmin):
    list_display = ('course','school','week_price', 'currency',)

    def currency(self,instance):
        return instance.week_price.currency
    
    currency.short_description = 'Currency'
    currency.admin_order_field = 'week_price_currency'

# Address being edited inside School 
"""
class AddressInLine(admin.TabularInline):
    model = Address
    
class SchoolAdmin(ShowIconBaseAdminModel):
    inlines = [
        AddressInLine,
    ]
"""    
class StateInLine(admin.TabularInline):
    model = State

class CountryAdmin(ShowIconBaseAdminModel):
    inlines = [
        StateInLine
    ]    

# Registering all models
admin.site.register(Country,CountryAdmin)
admin.site.register(City,ShowIconBaseAdminModel)
admin.site.register(Course,ShowIconBaseAdminModel)
# admin.site.register(School,SchoolAdmin)
admin.site.register(SchoolCourseValue,SchoolCourseValueModelAdmin)
# admin.site.register(State)
admin.site.register(CostOfLiving)
admin.site.register(HealthInsurrance)
