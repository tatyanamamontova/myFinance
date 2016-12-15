from django.db import models
from django.db.models import Avg
from django.db.models.functions import TruncMonth
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.forms import ValidationError


# Bank account
class Account(models.Model):

    account_holder = models.CharField(max_length=300, unique=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return str(self.account_holder)

    class Meta:
        db_table = 'charges'

    # def clean(self):
    #     cleaned_data = super(Account, self).clean()
    #     if self.total < 0:
    #         raise ValidationError('Not enough money')
    #     return cleaned_data

# Transaction
class Charge(models.Model):

    date = models.DateField()
    value = models.DecimalField(max_digits=6, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.date) + " : " + str(self.value) + " : " + str(self.account)

    @classmethod
    def get_incomes(cls, account):
        return cls.objects.filter(account=account).filter(value__gte=0)

    @classmethod
    def get_outcomes(cls, account):
        return cls.objects.filter(account=account).filter(value__lt=0)

    @classmethod
    def get_by_month(cls, account):
        return cls.objects\
            .filter(account=account)\
            .annotate(month=TruncMonth('date'))\
            .values('month')\
            .annotate(c=Avg('value'))\
            .values('month', 'c')


# define UserProfile
class User(AbstractUser):

    phone_number = models.CharField(max_length=30)
    adress = models.CharField(max_length=300, blank=True, null=True)


class UserEdit(models.Model):

    userprofile = models.CharField(max_length=300, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    adress = models.CharField(max_length=300, blank=True, null=True)


# class ChargeEdit(models.Model):
#
#     date = models.DateField()
#     value = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
