from django.contrib import admin
from .models import *
# Register your models here.

class VideoConferenceRecordAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'uid', 'room_name', 'call_duration']

admin.site.register(User)
admin.site.register(VideoConferenceRecord, VideoConferenceRecordAdmin)