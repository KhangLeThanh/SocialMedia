from django.contrib import admin
from funnysociety.models import SiteUser,Friend,Status,StatusComment,Discussion,Event,Participant



# Display properties of models in admin site
class SiteUserAdmin(admin.ModelAdmin):
    list_display = ['user','gender','telephone','birthdate']

class StatusAdmin(admin.ModelAdmin):
    list_display = ['user','text','timestamp']

class FriendAdmin(admin.ModelAdmin):
    list_display = ['party1','party2','timestamp','isPendingRequest','isReceivedRequest']



# Register your models here.
admin.site.register(SiteUser,SiteUserAdmin)
admin.site.register(Friend,FriendAdmin)
admin.site.register(Status,StatusAdmin)
admin.site.register(StatusComment)
admin.site.register(Discussion)
admin.site.register(Event)
admin.site.register(Participant)

