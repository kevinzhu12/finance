# Generated by Django 4.1.3 on 2023-01-10 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0011_uploadfile_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='file_name',
            field=models.TextField(default=None),
        ),
    ]
