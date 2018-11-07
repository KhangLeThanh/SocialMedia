from django.contrib import admin
from funnysociety.models import SiteUser,Friend,Status,StatusComment,Discussion,Event,Participant

# Register your models here.
admin.site.register(SiteUser)
admin.site.register(Friend)
admin.site.register(Status)
admin.site.register(StatusComment)
admin.site.register(Discussion)
admin.site.register(Event)
admin.site.register(Participant)

