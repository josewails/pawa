# Generated by Django 2.0.7 on 2018-07-12 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pamoja', '0005_surveyresult_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyresult',
            name='result',
            field=models.CharField(default='[[],[],[],[]]', max_length=1000),
        ),
    ]