from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import AccountHolderManager

CURRENCY_CHOICES = [(currency, currency) for currency in ['KZT', 'USD', 'EUR']]


class AccountHolder(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='AccountHolders/', null=True, blank=True)
    wallet = models.FloatField(default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='KZT')
    categories = models.ManyToManyField('Category', blank=True)
    expenses = models.ManyToManyField('Expense', blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountHolderManager()


class Category(models.Model):
    name = models.CharField(max_length=100)


class Expense(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    amount = models.FloatField()
    created_at = models.DateTimeField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
