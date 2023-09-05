from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("registration", views.register_request, name="register_request"),
    path("password_reset_done", views.password_reset_request, name="password_reset_done"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path('profile/', views.profile, name='profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('list_regist/', views.room_list_profile, name='list_regist')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)