from django.contrib import admin
from models import *

# Base Model to show real image of Icons intead of urls in forms
class ShowIconBaseAdminModel(admin.ModelAdmin):
    readonly_fields = ('icon_display',)
    
    def icon_display(self, instance):
        return u'<img src="%s" />' % instance.icon

    icon_display.short_description = 'Icon Display Image'
    icon_display.allow_tags = True

admin.site.register(Country,ShowIconBaseAdminModel)
admin.site.register(City,ShowIconBaseAdminModel)
admin.site.register(Course,ShowIconBaseAdminModel)
admin.site.register(School,ShowIconBaseAdminModel)
admin.site.register(SchoolCourseValue)

    
