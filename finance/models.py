from django.db import models


# Bank account
class Account(models.Model):

    account_id = models.CharField(max_length=300)
    income = models.DecimalField(max_digits=12, decimal_places=10)
    outcome = models.DecimalField(max_digits=12, decimal_places=10)
    total = models.DecimalField(max_digits=12, decimal_places=10)

    class Meta:
        db_table = 'charges'


# Transaction
class Charge(models.Model):

    date = models.DateField()
    value = models.DecimalField(max_digits=12, decimal_places=10)
    account = models.ForeignKey(Account, related_name='charge')