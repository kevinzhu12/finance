from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "expense/index.html")

def login(request):
    return render(request, "expense/login.html")

def logout(request):
    pass

def register(request):
    return render(request, "expense/register.html")
