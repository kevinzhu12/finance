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
    #redirects user to homepage when trying to visit login page if already logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "expense/login.html", {
                "message": "Invalid username and/or password"
            })
    else:
        return render(request, "expense/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    #redirects user to homepage when trying to visit register page if already logged in
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse("index"))

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

def month_view(request, month):
    #use month as some sort of model or filter all exepnses by this month and send that info to the month page
    return render(request, "expense/month.html", {
        "month": month
    })