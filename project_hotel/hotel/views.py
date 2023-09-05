
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Room, Reservation

from django.utils import timezone

from .forms import SearchForm, ReservationForm
from .utils import find_available_rooms

class Room_ListView(LoginRequiredMixin, generic.ListView):
    model = Room
    context_object_name = 'room_list'

    queryset = Room.objects.all()

    template_name = 'hotel/room_list_.html'

    paginate_by = 6


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'room_detail.html', {'room': room, 'pk': pk})


@login_required
def create_reservation(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.room = room
            reservation.save()
            reservation.add_to_profile.add(request.user)
            return render(request, 'reservation_detail.html', {'reservation': reservation})
    else:
        form = ReservationForm()

    return render(request, 'reservation_form.html', {'form': form})

def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservation_detail.html', {'reservation': reservation})


def user_reservation(request):
    reserv = Reservation.objects.filter(add_to_profile=request.user)
    #total_price = cart_items.aggregate(total=Sum(F('product__price') * F('quantity')))['total']
    return render(request, 'user_reservation.html', {'reserv': reserv})


def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.check_in_date > timezone.now().date():
        if request.user in reservation.add_to_profile.all():
            if request.method == 'POST':
                reservation.delete()
                return redirect('user_reserv')

            return render(request, 'reservation_delete.html', {'reservation': reservation})

    return redirect('reservation-detail', reservation_id=reservation_id)


def search_rooms(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            date_in = form.cleaned_data['date_in']
            date_out = form.cleaned_data['date_out']
            available_rooms = find_available_rooms(date_in, date_out)
            if date_out < date_in or date_in < timezone.now().date():
                form = SearchForm()
                return render(request, 'search_form.html', {'form': form})
            else:
                return render(request, 'search_results.html', {'available_rooms': available_rooms, 'date_in': date_in, 'date_out': date_out})
    else:
        form = SearchForm()
        return render(request, 'search_form.html', {'form': form})

def about_the_hotel(request):
    return render(request, 'about_the_hotel.html')