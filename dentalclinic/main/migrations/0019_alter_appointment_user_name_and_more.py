# Generated by Django 5.0 on 2024-03-19 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_appointment_user_comment_appointment_user_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='user_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='user_phone',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
