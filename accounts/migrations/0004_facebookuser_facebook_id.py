# Generated by Django 2.0.7 on 2018-07-21 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_facebookuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookuser',
            name='facebook_id',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
