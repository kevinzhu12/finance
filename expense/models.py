from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    pass


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userItems", default=None)
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=1000)
    desc = models.TextField(blank=True)
    loc = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name}: ${self.price}"


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userCategories", default=None)
    name = models.CharField(max_length=255, default=None)
    initial = models.CharField(max_length=1, validators=[MinLengthValidator(1, 'There must be a one letter initial')], default=None)
    #hex code for the color "#XXXXXX" as str selected through color wheel
    #dont need to worry about wrong str length? unless manually added through admin -- error
    color = models.CharField(max_length=7, default=None)

    def serialize(self):
        return {
            "name": self.name,
            "initial": self.initial,
            "color": self.color
        }

    def __str__(self):
        return f"{self.name} - {self.initial.upper()}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userExpenses", default=None)
    date = models.DateField(default=None)
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name="expenseDetails", default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="expensesUnderCategory", default=None)

    def __str__(self):
        return f"{self.user.username} - {self.date}{self.category.initial}: {self.item.name}"

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date.strftime('%m/%d/%Y'),
            "item": {"name": self.item.name, "price": self.item.price},
            "category": {"name": self.category.name, "initial": self.category.initial, "color": self.category.color}
        }


class UploadFile(models.Model):
    def user_path_directory(self, filename):
        return f'uploads/{self.user.username}/{filename}'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploadedFiles")
    file = models.FileField(upload_to=user_path_directory)
    file_name = models.TextField(default=None)
    date = models.DateField(default=None)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.file_name}'

    def serialize(self):
        return {
            "file_name": self.file_name,
            "date": self.date,
            "selected": self.selected,
            "file_id": self.id
        }

