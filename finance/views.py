from django.shortcuts import render, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .forms import ChargeForm, CreateAccount, CreateTransaction
from .models import Account, Charge #CreateAccount
from django.db.models import F

# from models.RandomTransactions import random_transactions
# from models.Charge import Charge

from django.utils import timezone
from datetime import datetime


def index(request):
    form = ChargeForm(request.POST)
    return render(request, 'index.html', {'form': form})


def charges(request, account_holder):

    account = Account.objects.get(account_holder=account_holder)

    incomes = Charge.get_incomes(account)
    outcomes = Charge.get_outcomes(account)

    return render(request, 'charges.html', {'account': account,
                                            'incomes': incomes,
                                            'outcomes': outcomes})
    return HttpResponse("Charges")


def create_account(request):

    if request.method == 'POST':
        form = CreateAccount(request.POST)
        if form.is_valid():
            account = Account(account_holder=form.cleaned_data["account_holder"],
                              income=0,
                              outcome=0,
                              total=0)
            account.save()
            return HttpResponse(form.cleaned_data["account_holder"])
        else:
            return HttpResponse("Not valid")

    return render(request, 'create_account.html')


def create_charge(request, account_holder):

    account = Account.objects.get(account_holder=account_holder)

    if request.method == 'POST':
        form = CreateTransaction(request.POST)
        if form.is_valid():
            charge = Charge(account=account,
                            value=form.cleaned_data['transaction'],
                            date=timezone.datetime.now())
            charge.save()
            Account.objects.filter(account_holder=account_holder)\
                .update(total=F('total') + form.cleaned_data['transaction'])
            return HttpResponse("Done")

        return HttpResponse("Error")

    return render(request, 'charge.html')


def get_all_accounts(request):
    all_accounts = Account.objects.get_queryset()
    print("All accounts: ")
    print(all_accounts)
    return render(request, 'all_accounts.html', {'all_accounts' : all_accounts})


def account_view(request, account_holder):

    account = Account.objects.get(account_holder=account_holder)

    if request.method == 'POST':
        form = CreateTransaction(request.POST)
        if form.is_valid():
            charge = Charge(account=account,
                            value=form.cleaned_data['transaction'],
                            # date=timezone.datetime.now())
                            date = datetime(2015, 6, 10))
            charge.save()
            Account.objects.filter(account_holder=account_holder)\
                .update(total=F('total') + form.cleaned_data['transaction'])
            return HttpResponse("POST OK")
        return HttpResponse("Method POST")

    else:
        try:
            outcomes = Charge.get_outcomes(account)
            incomes = Charge.get_incomes(account)
            months = Charge.get_by_month(account)
            print(months)
        except ObjectDoesNotExist:
            print("Can't find")
        return render(request, 'account.html', {'account': account,
                                                'incomes': incomes,
                                                'outcomes': outcomes,
                                                'months': months})


def months(request, account_holder):

    try:
        account = Account.objects.get(account_holder=account_holder)
        by_months = Charge.get_by_month(account)
    except ObjectDoesNotExist:
        print("Can't find")
    return render(request, 'months.html', {'account': account, 'months': by_months})