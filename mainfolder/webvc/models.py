from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class VideoConferenceRecord(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='created_user')
    joined_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='joined_user')
    room_name = models.CharField(max_length=200, null=True)
    call_duration = models.FloatField(null=True) 

    def __str__(self):
        return self.room_name
