# Generated by Django 3.2.9 on 2021-12-22 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='staff',
        ),
        migrations.AddField(
            model_name='customuser',
            name='identifier',
            field=models.CharField(max_length=40, null=True, unique=True),
        ),
    ]
