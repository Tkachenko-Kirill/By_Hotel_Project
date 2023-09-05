# Generated by Django 4.2.4 on 2023-08-28 14:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotel', '0002_reservation_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='add_to_profile',
            field=models.ManyToManyField(blank=True, related_name='user_reserv', to=settings.AUTH_USER_MODEL),
        ),
    ]
