from django.db import models
from django.shortcuts import reverse

from django.contrib.auth.models import User

from django.utils import timezone
import datetime

class Room(models.Model):
    title = models.CharField(max_length = 200)
    number = models.IntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sleeping_places = models.IntegerField(default=1, choices=[(i, int(i)) for i in range(1, 6)])
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('room-detail', kwargs={'pk': self.pk})

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length = 100, default='Guest')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    is_active = models.BooleanField(default=True)
    add_to_profile = models.ManyToManyField(User, related_name='user_reserv', blank=True,)

    def __str__(self):
        return self.guest_name

    def get_absolute_url(self):
        return reverse('reservation-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.check_out_date < timezone.now().date():
            self.is_active = False
        existing_reservations = Reservation.objects.filter(room=self.room, is_active=True)
        for reservation in existing_reservations:
            if reservation.check_in_date <= self.check_in_date <= reservation.check_out_date or reservation.check_in_date <= self.check_out_date <= reservation.check_out_date:
                raise Exception("Room is already reserved for the specified dates")
        super().save(*args, **kwargs)


class RoomImage(models.Model):
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)
    product = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in RoomImage._meta.fields]

