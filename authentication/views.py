import logging
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate

from . import forms

logger = logging.getLogger("django")

def logout_user(request):
    if 'years' in request.session.keys():
        del request.session['years']
    logout(request)
    return redirect('login')

def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                request.session['years'] = []
                if request.GET.get('next') is not None:
                    return HttpResponseRedirect(request.GET['next'])
                message = f'Hello {user.username}! You have been logged in'
            else:
                message = 'Login failed!'
    return render(request, 'authentication/login.html', context={'form': form, 'message': message})

def registration_page(request):
    form = forms.RegisterForm()
    message = None
    error_msg = None
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['username']
            form.save()
            message = f'Hello {new_username}! You have been registered'
        else:
            error_msg = (str)(form.errors)
    return render(request, 'authentication/register.html', context={'form': form, 'message': message, 'error_msg': error_msg})