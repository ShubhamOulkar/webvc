# Generated by Django 4.2 on 2023-06-19 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webvc', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoconferencerecord',
            name='joined_by',
        ),
        migrations.AddField(
            model_name='videoconferencerecord',
            name='uid',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
