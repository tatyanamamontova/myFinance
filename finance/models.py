from django.db import models
from django.db.models import Avg
from django.db.models.functions import TruncMonth


# Bank account
class Account(models.Model):

    account_holder = models.CharField(max_length=300, unique=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.account_holder)

    class Meta:
        db_table = 'charges'


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
