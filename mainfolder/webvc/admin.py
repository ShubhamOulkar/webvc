from django.contrib import admin
from .models import *
# Register your models here.

class VideoConferenceRecordAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'joined_by', 'room_name', 'call_duration']

admin.site.register(User)
admin.site.register(VideoConferenceRecord, VideoConferenceRecordAdmin)