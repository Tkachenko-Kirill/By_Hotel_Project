from django.db.models import Q
from datetime import date
from .models import Room, Reservation

def find_available_rooms(date_in, date_out):
    # Найти все комнаты, у которых нет активных резерваций на указанные даты
    reserved_rooms = Reservation.objects.filter(
        Q(check_in_date__lte=date_in, check_out_date__gte=date_in) | # Пересекаются с началом брони
        Q(check_in_date__lte=date_out, check_out_date__gte=date_out) | # Пересекаются с окончанием брони
        Q(check_in_date__gte=date_in, check_out_date__lte=date_out) # Включены внутри периода брони
    ).values_list('room', flat=True)

    # Исключить зарезервированные комнаты из списка всех комнат
    available_rooms = Room.objects.exclude(id__in=reserved_rooms)

    return available_rooms