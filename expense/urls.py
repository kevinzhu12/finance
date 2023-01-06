from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("month/<str:month>", views.month_view, name="month"),
    path("create_category", views.create_category, name="create_category"),
    path("update_category/<int:category_id>", views.update_category, name="update_category"),
    path("add_expense", views.add_expense, name="add_expense"),
    path("delete_expense/<int:expense_id>", views.delete_expense, name="delete_expense"),
    path("get_expenses", views.get_expenses, name="get_expenses")
]
