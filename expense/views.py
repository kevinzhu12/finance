import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from .models import User, Category, Item, Expense
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, "expense/index.html", {
            "categories": Category.objects.filter(user=request.user).order_by("name"),
            "expenses": Expense.objects.filter(user=request.user).order_by("date")
        })
    else:
        return HttpResponseRedirect(reverse("login"))

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

def get_categories(request):
    categories = Category.objects.all().order_by('initial')
    listOfCategories = [f'{category.initial} - {category.name}' for category in categories]

    return JsonResponse({"categories": listOfCategories})

def create_category(request):
    if request.method == "POST":
        name = request.POST['name'].capitalize()
        initial = request.POST['initial'].capitalize()
        color = request.POST['color']

        #check if name, initial, or color already exist in a category
        categories = Category.objects.filter(user=request.user)

        #stop function prematurely if any of these vars are already in-use
        for category in categories:
            if category.name == name or category.initial == initial or category.color == color:
                #already exists
                return HttpResponseRedirect(reverse('index'))

        #if none of these are true -- run this -- should i do a for-else loop? seems right but not necessary?
        newCategory = Category(user=request.user, name=name, initial=initial, color=color)
        newCategory.save()
    
    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def update_category(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return JsonResponse({"error": "Category not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(category.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)

        if data.get("delete"):
            category.delete()
            return HttpResponse(status=204)

        newName = data['name'].capitalize()
        newInitial = data['initial'].capitalize()
        newColor = data['color']

        if data.get("name").capitalize() != category.name and Category.objects.filter(name=newName).count() == 0:
            category.name = newName
        if data.get("initial").capitalize() != category.initial and Category.objects.filter(initial=newInitial).count() == 0:
            category.initial = newInitial
        if data.get("color") != category.color and Category.objects.filter(color=newColor).count() == 0:
            category.color = newColor
        category.save()

        return HttpResponse(status=202)



#do it as a rerender of the page for now -- maybe change to js later so no need to reload page
def add_expense(request):
    if request.method == "POST":
        newItem = Item(user=request.user, name=request.POST['name'], price=request.POST['price'], desc=request.POST['description'], loc=request.POST['location'])
        newItem.save()
        newExpense = Expense(user=request.user, date=request.POST['date'], item=newItem, category=Category.objects.get(initial=request.POST['category']))
        newExpense.save()

    return HttpResponseRedirect(reverse('index'))


def delete_expense(request, expense_id):
    print(expense_id)
    Expense.objects.get(pk=expense_id).delete()
    return HttpResponse(status=204)


def get_expenses(request):
    if request.user.is_authenticated:
        userExpenses = Expense.objects.filter(user=request.user).order_by("date")
        data = [expense.serialize() for expense in userExpenses]

        return JsonResponse({
            "expenses": data
        })
    
    return JsonResponse({
        "error": "not signed in"
    })

@csrf_exempt
def update_expense(request, expense_id):
    try:
        targetExpense = Expense.objects.get(pk=expense_id)
        targetItem = targetExpense.item
    except:
        return JsonResponse({"error": "Cannot find expense"}, status=404)
    
    updateInfo = json.loads(request.body)
    
    if updateInfo.get("name") is not None:
        targetItem.name = updateInfo['name']
    if updateInfo.get("price") is not None:
        targetItem.price = updateInfo['price']
    if updateInfo.get("desc") is not None:
        targetItem.desc = updateInfo['desc']
    if updateInfo.get("loc") is not None:
        targetItem.loc = updateInfo['loc']
    if updateInfo.get('date') is not None:
        targetExpense.date = updateInfo['date']
    if updateInfo.get('category') is not None:
        updateCategory = Category.objects.get(initial=updateInfo['category'][:1])
        targetExpense.category = updateCategory        

    targetItem.save()
    targetExpense.save()

    return HttpResponse(status=204)


def upload(request):
    data = []
    if request.method == "POST":
        try:
            csv_file = request.FILES['filename']
            if not csv_file.name.endswith('.csv'):
                return HttpResponseRedirect(reverse('upload'))
            
            file_data = csv_file.read().decode("utf-8")

            lines = file_data.split('\n')
            for line in lines:
                items = line.split(',')
                for i in range(len(items)):
                    if i % 3 == 0:
                        data_dict = dict()
                        dateExp = items[i]
                        if dateExp == "":
                            continue
                        data_dict['name'] = items[i + 2]
                        data_dict['price'] = "" if items[i + 1] == "" else float(items[i + 1][1:])
                        data_dict['date'] = dateExp[:len(dateExp) - 1]
                        data_dict['category'] = dateExp[len(dateExp) - 1:]
                        data.append(data_dict)
        except:
            return HttpResponseRedirect(reverse('upload'))
        
    return render(request, 'expense/upload.html')