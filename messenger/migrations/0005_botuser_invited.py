# Generated by Django 2.0.7 on 2018-07-25 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0004_auto_20180715_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='invited',
            field=models.IntegerField(default=False),
        ),
    ]
