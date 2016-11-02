from django.shortcuts import render

from .forms import ChargeForm

from models.RandomTransactions import random_transactions
from models.Charge import Charge


def index(request):
    form = ChargeForm(request.POST)
    return render(request, 'index.html', {'form': form})


def charges(request):
    transactions = random_transactions()
    positive = list()
    negative = list()
    for each in transactions:
        if each[1] > 0:
            positive.append(each)
        else:
            negative.append(each)

    return render(request, 'charges.html', {'positive': positive,
                                            'negative': negative})
