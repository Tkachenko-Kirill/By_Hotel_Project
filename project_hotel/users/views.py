from django.shortcuts import render, redirect
from .forms import PasswordResetForm, NewUserForm, UserSelectForm, ProfileForm
from django.db.models.query_utils import Q

from .models import User, Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#password reset
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import login, logout

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            user_email = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=user_email)).first()
            if associated_users:
                subject = "Восстановление пароля"
                email_template_name = "password_reset_email.html"
                c = {
                    "email": associated_users.email,
                    'domain': get_current_site(request).domain,
                    "uid": urlsafe_base64_encode(force_bytes(associated_users.pk)),
                    "user": associated_users,
                    'token': default_token_generator.make_token(associated_users),
                    'protocol': 'https' if request.is_secure() else 'http',
                }
                email = render_to_string(email_template_name, c)
                print(email)
                try:
                    print('Запускаю функцию сенд_емаил')
                    send_mail(subject, email, 'sayt.pitstseriya@mail.ru', [associated_users.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Ошибка.')
                return redirect ("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html", context={"form":password_reset_form})

def password_reset_done(request):
    return render(request, 'password_reset_done.html')

def passwordResetConfirm(request, uidb64, token):
    return redirect("home")

def register_request(request):
    if not Group.objects.filter(name='Customer').exists():
        Group.objects.create(name='Customer')

    customer_group = Group.objects.get(name='Customer')
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(customer_group)
            user.save()

            new_profile = Profile.objects.create(user = user, username = user.username)
            new_profile.save()

            login(request, user)
            messages.success(request, "Регистрация прошла успешно")
            return redirect('home')
        else:
            messages.error(request, "Ошибка. Неверно введенная информация")

    form = NewUserForm()
    return render(request, 'registration_page.html', context={'registration_form': form})

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_username = form.cleaned_data['username']  # Подставьте поле из вашей формы
            if new_username != request.user.username:
                # Проверка, чтобы избежать лишних изменений
                request.user.username = new_username
                request.user.save()
            form.save()
            return redirect('profile')

    return render(request, 'profile.html', {'profile':profile, 'form': form})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Профиль успешно удален')
        logout(request)
        return redirect('login')

def add_book_to_profile(request):
    current_user = User.objects.get(id=request.user.id)

    room_list = current_user.user_reserv.all()

    context = {
        'room_list': room_list
    }
    return render(request, 'profile/user_room_list.html', context=context)

def room_list_profile(request):
    current_user = User.objects.get(id=request.user.id)

    room_list = current_user.user_reserv.all()

    context = {
        'room_list': room_list
    }
    return render(request, 'user_room_list.html', context=context)