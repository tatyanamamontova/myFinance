from django.shortcuts import render, HttpResponse, redirect, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from .forms import ChargeForm, CreateAccount, LoginForm, UserProfileForm
from .models import Account, Charge, UserProfile
from django.db.models import F
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#Enter to system
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
            return redirect('profile_view', username = username)
    context = {'form': user_form}
    return render(request,'login.html', context)


#Exit
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/')

#Registration
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
                                                    phone_number = phone_number,
                                                    adress = adress)
            user.set_password(password)
            user.save()
            return redirect('user/(?P<username>\w+)', username)
        else:
            return HttpResponse('Errors!')
    context = {'form': user_form}
    return render(request,'registration.html', context)



#Profile view
@login_required
def profile_view(request,username):
    profile = UserProfile.objects.get(username = username)
    return render(request, 'profile.html', {'profile':profile})

#Charges of account
def charges(request, account_holder):

    account = Account.objects.get(account_holder=account_holder)
    incomes = Charge.get_incomes(account)
    outcomes = Charge.get_outcomes(account)
    return render(request, 'charges.html', {'account': account,
                                            'incomes': incomes,
                                            'outcomes': outcomes})
    return HttpResponse("Charges")

#Create the account
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

#Create the charge
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

#All accounts
def get_all_accounts(request):
    all_accounts = Account.objects.get_queryset()
    print("All accounts: ")
    print(all_accounts)
    return render(request, 'all_accounts.html', {'all_accounts' : all_accounts})

#Account view
def account_view(request, account_holder):

    account = Account.objects.get(account_holder=account_holder)
    outcomes = Charge.get_outcomes(account)
    incomes = Charge.get_incomes(account)
    months = Charge.get_by_month(account)
    return render(request, 'account.html', {'account': account,
                                            'incomes': incomes,
                                            'outcomes': outcomes,
                                            'months': months})

#Charges by months
def months(request, account_holder):

    try:
        account = Account.objects.get(account_holder=account_holder)
        by_months = Charge.get_by_month(account)
    except ObjectDoesNotExist:
        print("Can't find")
    return render(request, 'months.html', {'account': account, 'months': by_months})