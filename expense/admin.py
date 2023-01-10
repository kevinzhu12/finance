from django.contrib import admin

from .models import User, Item, Category, Expense, UploadFile

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(UploadFile)