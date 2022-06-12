# Generated by Django 4.0.3 on 2022-05-30 15:57

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boost',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='core',
            name='level',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'Такой пользователь уже зарегестрирован.'}, help_text='', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
