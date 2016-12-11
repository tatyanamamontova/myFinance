from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import ChargeForm, CreateAccount, LoginForm, UserProfileForm
from .models import Account, Charge, UserProfile
from django.contrib.auth.models import Permission
from django.db.models import F
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import (login_required, permission_required)


# Enter to system
def login_view(request):
    user_form = LoginForm()
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if not user:
                info = 'The username and password were incorrect'
                return render(request, 'login.html', {'info': info})
            login(request, user)
            return redirect('profile_view', username=username)
    context = {'form': user_form}
    return render(request, 'login.html', context)


# Exit
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/')


# Registration
def registration(request):
    user_form = UserProfileForm()
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            phone_number = user_form.cleaned_data['phone_number']
            adress = user_form.cleaned_data['adress']
            user = UserProfile.objects.create_user(username=username,
                                                   phone_number=phone_number,
                                                   adress=adress)
            user.set_password(password)
            user.save()

            return redirect('user/(?P<username>\w+)', username)
        else:
            return HttpResponse('Errors!')
    context = {'form': user_form}
    return render(request, 'registration.html', context)


# Profile view
@login_required
def profile_view(request, username):
    profile = UserProfile.objects.get(username=username)
    return render(request, 'profile.html', {'profile': profile})


# Create the account
@login_required
def create_account(request, username):
    user = UserProfile.objects.get(username=username)
    form = CreateAccount()
    if request.method == 'POST':
        form = CreateAccount(request.POST)
        if form.is_valid():
            with transaction.atomic():
                account_holder = form.cleaned_data['account_holder']
                account = Account(user=user, account_holder=account_holder, total=0)
                account.save()
            return redirect('account_view', username, account_holder)
        else:
            return HttpResponse("Not valid")
    context = {'form': form}
    return render(request, 'create_account.html', context, {'user': user})

# Account view
@login_required
def account_view(request, username, account_holder):
    user = UserProfile.objects.get(username=username)
    account = Account.objects.get(user=user, account_holder=account_holder)
    outcomes = Charge.get_outcomes(account)
    incomes = Charge.get_incomes(account)
    months = Charge.get_by_month(account)
    return render(request, 'account.html', {'user': user,
                                            'account': account,
                                            'incomes': incomes,
                                            'outcomes': outcomes,
                                            'months': months})


# All user's accounts
@login_required
def get_all_accounts(request, username):
    user = UserProfile.objects.get(username=username)
    all_accounts = Account.objects.filter(user=user)
    print("All accounts: ")
    print(all_accounts)
    return render(request, 'all_accounts.html', {'all_accounts': all_accounts,
                                                 'user': user})


# Charges of account
@login_required
def charges(request, username, account_holder):
    user = UserProfile.objects.get(username=username)
    account = Account.objects.get(user=user, account_holder=account_holder)
    incomes = Charge.get_incomes(account)
    outcomes = Charge.get_outcomes(account)
    return render(request, 'charges.html', {'user': user,
                                            'account': account,
                                            'incomes': incomes,
                                            'outcomes': outcomes})


# Create the charge
@login_required
def create_charge(request, username, account_holder):
    user = UserProfile.objects.get(username=username)
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
                Account.objects.filter(user=user, account_holder=account_holder) \
                    .update(total=F('total') + form.cleaned_data['value'])
            return redirect('account_view',username, account_holder)
    context = {'account': account_holder, 'form': form}
    return render(request, 'charge.html', context)



# Charges by months
@login_required
def months(request, username, account_holder):
    try:
        user = UserProfile.objects.get(username=username)
        account = Account.objects.get(user=user, account_holder=account_holder)
        by_months = Charge.get_by_month(account)
    except ObjectDoesNotExist:
        print("Can't find")
    return render(request, 'months.html', {'user': user,'account': account, 'months': by_months})
