# Generated by Django 3.0.2 on 2020-02-12 11:09

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pv', '0005_auto_20200211_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pv',
            name='Date_recieved',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today)]),
        ),
        migrations.AlterField(
            model_name='pv',
            name='Date_returned',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today)]),
        ),
    ]