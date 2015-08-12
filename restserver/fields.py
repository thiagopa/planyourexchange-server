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
from restserver.models import *
from rest_framework import serializers
from djmoney.models.fields import MoneyField
from django.utils.encoding import smart_text
from moneyed import Money

class MoneyField(serializers.Field):
    """
        Representation of money with value and default currency
        that would be changed automatically by the country's default
    """
    def to_representation(self, obj):
        return obj.amount

    def to_internal_value(self, data):
        amount = smart_text(data).strip()
        return Money(amount)
