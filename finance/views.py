from django.shortcuts import render, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .forms import ChargeForm, CreateAccount
from .models import Account, Charge
from django.db.models import F


def charges(request, account_holder):

    account = Account.objects.get(account_holder=account_holder)
    incomes = Charge.get_incomes(account)
    outcomes = Charge.get_outcomes(account)
    return render(request, 'charges.html', {'account': account,
                                            'incomes': incomes,
                                            'outcomes': outcomes})
    return HttpResponse("Charges")


def create_account(request):
    form = CreateAccount()
    if request.method == 'POST':
        form = CreateAccount(request.POST)
        if form.is_valid():
            account = Account(account_holder=form.cleaned_data['account_holder'], total=0)
            account.save()

            return HttpResponse(form.cleaned_data['account_holder'])
        else:
             return HttpResponse("Not valid")
    context = {'form': form}
    return render(request, 'create_account.html',context)


def create_charge(request, account_holder):
    account = Account.objects.get(account_holder=account_holder)
    form = ChargeForm()
    if request.method == 'POST':
        form = ChargeForm(request.POST)
        if form.is_valid():
            charge = Charge(account=account,
                            date=form.cleaned_data['date'],
                            value=form.cleaned_data['value'])
            charge.save()
            Account.objects.filter(account_holder=account_holder).update(total=F('total') + form.cleaned_data['value'])
            return HttpResponse("Done")
        return HttpResponse("Error")
    context = {'form':form}
    return render(request, 'charge.html', context)


def get_all_accounts(request):
    all_accounts = Account.objects.get_queryset()
    print("All accounts: ")
    print(all_accounts)
    return render(request, 'all_accounts.html', {'all_accounts' : all_accounts})


def account_view(request, account_holder):

    account = Account.objects.get(account_holder=account_holder)
    outcomes = Charge.get_outcomes(account)
    incomes = Charge.get_incomes(account)
    months = Charge.get_by_month(account)
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