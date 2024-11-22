from django.shortcuts import render, reverse, redirect
from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserForm, UserUpdateForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def user_register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        new_user = form.save()
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return HttpResponseRedirect(reverse('users:login_user'))

    return render(request, 'users/register_user.html', {'form': UserRegisterForm})


def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('users:profile_user'))
                else:
                    return HttpResponse('Disabled account')
    else:
        form = UserLoginForm()
        return render(request, 'users/login_user.html', {'form': form})


@login_required
def user_profile_view(request):
    user_object = request.user
    context = {
        # 'user_object': user_object,
        'title': f'Профиль пользователя {user_object.first_name}',
        # 'form': UserForm(instance=user_object),
    }

    return render(request, 'users/user_profile_read_only.html', context)


@login_required
def user_udate_view(request):
    user_object = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            user_object = form.save()
            user_object.save()
            return redirect('users:profile_user')
    user_name = user_object.first_name
    context = {
    'user_object': user_object,
    'title': f' Изменить профиль пользователя {user_name}',
    'form': UserUpdateForm(instance=user_object),
    }
    return render(request, 'users/update_user.html', context)

def user_logout_view(request):
    logout(request)
    return redirect('dogs:index')
