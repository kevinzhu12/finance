# Generated by Django 4.1.3 on 2022-12-24 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0003_alter_itembought_itemloc_alter_itembought_itemname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemName', models.CharField(max_length=255)),
                ('itemPrice', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('itemDesc', models.TextField(blank=True)),
                ('itemLoc', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='ItemBought',
        ),
    ]