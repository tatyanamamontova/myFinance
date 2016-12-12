from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist

from .forms import ChargeForm, CreateAccount
from .models import Account, Charge, User
from .serializers import AccountSerializer, MonthStatCollection
from django.db.models import F
from django.db import transaction

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
            with transaction.atomic():
                account_holder = form.cleaned_data['account_holder']
                account = Account(account_holder=account_holder, total=0)
                account.save()

            return redirect('account_view', account_holder)
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
            with transaction.atomic():
                charge = Charge(account=account,
                                date=form.cleaned_data['date'],
                                value=form.cleaned_data['value'])
                charge.save()
                Account.objects.filter(account_holder=account_holder)\
                    .update(total=F('total') + form.cleaned_data['value'])
            return redirect('account_view', account_holder=account_holder)
    context = {'account': account_holder, 'form':form}
    return render(request, 'charge.html', context)


# @login_required
def get_all_accounts(request):
    all_accounts = Account.objects.get_queryset()
    print("All accounts: ")
    print(all_accounts)
    return render(request, 'all_accounts.html', {'all_accounts' : all_accounts})


@login_required(redirect_field_name='all_accounts')
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


@api_view(['GET'])
def serialized_get_all_accounts(request):
    all_accounts = Account.objects.all()
    serializer = AccountSerializer(all_accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def serialized_account_view(request, account_holder):
    account = Account.objects.get(account_holder=account_holder)
    serializer = AccountSerializer(account)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def serialized_months(request, account_holder):
    test = MonthStatCollection(account_holder)
    return test.get(request)


def login_view(request):
    print(User.objects.get_queryset()[1].username)
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not (username and password):
        return render(request, 'login.html')
    user = authenticate(username=username, password=password)
    if not user:
        # error('Wrong credentials!')
        print(username)
        print(password)
        print("error!")
        return render(request, 'login.html')
    login(request, user)
    return redirect('all_accounts')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('all_accounts')
    return render(request, 'logout.html')