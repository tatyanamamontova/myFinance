from django.db import models


class Charge(models.Model):  # денежная транзакция

    date = models.DateField(label='date')
    value = models.DecimalField(label='value')
    account = models.ForeignKey(Account, related_name='charge')


class Account(models.Model):  # банковский счет

    account_id = models.CharField(max_length=300)
    income = models.DecimalField(label='income')
    outcome = models.DecimalField(label='outcome')
    total = models.DecimalField(label='total')

    class Meta:
        db_table1 = 'income'
        db_table2 = 'outcome'
