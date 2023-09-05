from django.urls import path, re_path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path(r'rooms/', views.Room_ListView.as_view(), name='rooms'),
    path(r'rooms/<pk>', views.room_detail, name='room-detail'),
    path(r'my_reservations', views.user_reservation, name='user_reserv'),
    path('create_reservation/<int:room_id>/', views.create_reservation, name='create-reservation'),
    path('reservation/<int:reservation_id>/delete/', views.delete_reservation, name='delete-reservation'),
    path('reservation/<int:reservation_id>/', views.reservation_detail, name='reservation-detail'),

    path('search/', views.search_rooms, name='search'),

    path('about', views.about_the_hotel, name='about-the-hotel')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)