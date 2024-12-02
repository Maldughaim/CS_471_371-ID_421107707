from django.shortcuts import render,redirect
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
import requests

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("users.login_user")  # Use the name of the login URL pattern
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = SignUpForm()

    return render(request, "usermodule/register.html", {"form": form,'messages':messages.get_messages(request)})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Validate user credentials
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f'Attempting to authenticate user: {username}\n{password}')
            user = authenticate(request, username=username, password=password)
            print(f'User authentication result: {user}')
            if user is not None:
                login(request, user)  # Log the user in
                print('here')
                return redirect('/books/lab10/task3/listimages/')  # Redirect to home or dashboard
            else:
                print('here2')
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Form is not valid. Please try again.')
    elif request.method == 'GET' and 'next' in request.GET:
        messages.error(request,'You must login to access this page')
        form = LoginForm()

    else:
        form = LoginForm()

    return render(request, 'usermodule/login.html', {'form': form,'messages':messages.get_messages(request)})

def logout_user(request):
    logout(request)
    messages.error(request, 'You have been loged out!')
    return redirect('users.login_user')