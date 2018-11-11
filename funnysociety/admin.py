from django.contrib import admin
from funnysociety.models import SiteUser,Friend,Status,StatusComment,Discussion,Event,Participant


class SiteUserAdmin(admin.ModelAdmin):
    list_display = ['user','gender','telephone','birthdate']

class StatusAdmin(admin.ModelAdmin):
    list_display = ['user','text','timestamp']



# Register your models here.
admin.site.register(SiteUser,SiteUserAdmin)
admin.site.register(Friend)
admin.site.register(Status,StatusAdmin)
admin.site.register(StatusComment)
admin.site.register(Discussion)
admin.site.register(Event)
admin.site.register(Participant)

