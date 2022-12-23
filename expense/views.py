from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, "expense/index.html", {
        })
    else:
        return render(request, "expense/login.html")

def login_view(request):
    return render(request, "expense/login.html")

def logout_view(request):
    pass

def register(request):
    if request.method == "POST":
        print(request.POST)

        username = request.POST['username']
        email = request.POST['email']

        #check if the passwords match
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, "expense/register.html", {
                "message": "Passwords must match."
            })

        #attempt to create the account for the user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "expense/register.html", {
                "message": "Username is already taken"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "expense/register.html")
