# Generated by Django 2.0.7 on 2018-07-15 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pamoja', '0008_auto_20180713_1022'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GroupAdmin',
        ),
        migrations.AlterField(
            model_name='group',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
