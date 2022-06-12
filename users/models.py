import django.contrib.auth.models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import users
from copy import copy
from .constants import BOOST_TYPE_CHOICES, BOOST_TYPE_VALUES, CASUAL_BOOSTS_VALUES


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            ""
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("Такой пользователь уже зарегестрирован."),
        },
    )


class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Core(models.Model):
    user = models.OneToOneField(
        User,
        null=False,
        on_delete=models.CASCADE
    )
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    auto_click_power = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    def update_coins(self, coins, commit=True):
        self.coins = coins
        is_levelupdated = self.is_levelup()
        boost_type = self.get_boost_type()

        if is_levelupdated:
            self.level += 1
        if commit:
            self.save()

        return is_levelupdated, boost_type

    def get_boost_type(self):
        boost_type = 0
        if self.level % 3 == 0:
            boost_type = 1
        return boost_type

    def is_levelup(self):
        return self.coins >= self.calculate_next_level_price()

    def calculate_next_level_price(self):
        return (self.level ** 2) * 10 * self.level


class Boost(models.Model):
    core = models.ForeignKey(Core, null=False, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    price = models.IntegerField(default=10)
    power = models.IntegerField(default=1)
    type = models.PositiveSmallIntegerField(default=0, choices=BOOST_TYPE_CHOICES)

    def levelup(self, coins):

        if coins < self.price:
            return False

        self.core.coins = coins - self.price
        self.core.click_power += self.power * BOOST_TYPE_VALUES[self.type]['click_power_scale']
        self.core.auto_click_power += self.power * BOOST_TYPE_VALUES[self.type]['auto_click_power_scale']
        self.core.save()


        old_boost_values = copy(self)
        self.level += 1
        self.price = round(self.price * 1.55)
        self.save()

        return old_boost_values, self
