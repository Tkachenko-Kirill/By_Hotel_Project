from django.contrib import admin

from .models import Room, RoomImage, Reservation

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

class ReservationAdmin(admin.ModelAdmin):
    pass

class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline]

class RoomImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Room, RoomAdmin)
admin.site.register(RoomImage, RoomImageAdmin)
admin.site.register(Reservation, ReservationAdmin)
