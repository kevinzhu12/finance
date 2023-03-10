# Generated by Django 4.1.3 on 2022-12-24 05:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0004_item_delete_itembought'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='itemDesc',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='itemLoc',
            new_name='loc',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='itemName',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='itemPrice',
            new_name='price',
        ),
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(default=None, max_length=7),
        ),
        migrations.AddField(
            model_name='category',
            name='initial',
            field=models.CharField(default=None, max_length=1, validators=[django.core.validators.MinLengthValidator(1, 'There must be a one letter initial')]),
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='expense',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='expenseUnderCategory', to='expense.category'),
        ),
        migrations.AddField(
            model_name='expense',
            name='date',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='expense',
            name='item',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='expenseDetails', to='expense.item'),
        ),
        migrations.AddField(
            model_name='expense',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='userExpenses', to=settings.AUTH_USER_MODEL),
        ),
    ]
