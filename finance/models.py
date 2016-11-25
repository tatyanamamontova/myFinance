from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth


# Bank account
class Account(models.Model):

    account_holder = models.CharField(max_length=300)
    income = models.DecimalField(max_digits=6, decimal_places=2)
    outcome = models.DecimalField(max_digits=6, decimal_places=2)
    total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.account_holder)

    class Meta:
        db_table = 'charges'


# Validate account creation
# class CreateAccount(ModelForm):
#
#     class Meta:
#         model = Account
#         fields = ['account_id','income','outcome']
#
#     def clean_account_id(self):
#         id = self.cleaned_data.get('account_id')
#         if id != "One":
#             raise ValidationError("Not valid")
#         return id


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