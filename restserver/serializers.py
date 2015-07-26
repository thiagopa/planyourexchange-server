from django.contrib.auth.models import User, Group
from restserver.models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
        
class CountrySerializer(serializers.HyperlinkedModelSerializer):
    
    #icon = serializers.SerializerMethodField('get_image_url')
    
    class Meta:
        model = Country
        
    #def get_image_url(self, obj):
    #    return obj.icon.url