from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import ChargeForm, CreateAccount, LoginForm, UserProfileForm, UserProfileEdit
from .models import Account, Charge, User
from .forms import ChargeForm, CreateAccount
from .models import Account, Charge
from .serializers import AccountSerializer, MonthStatCollection, UserSerializer, ChargeSerializer
from django.db.models import F
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache, cache_control

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create_superuser in terminal username = 'admin', password = 'qwerty1234'


# For checking users
def user_view(view_func):
    def wrapped(request, username, *args, **kwargs):
        user = User.objects.get(username=username)
        if request.user.username == username or request.user.is_superuser:
            return view_func(request, username,  *args, **kwargs)
        else:
            return redirect('logout')
    return wrapped


# Main page
def main_page(request):
    return render(request, 'main_page.html')


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
            if user.is_superuser:
                return redirect ('all_users')
            else:
                return redirect('profile_view', username=username)
    context = {'form': user_form}
    return render(request, 'login.html', context)


# Exit
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return render(request, 'logout.html')


# Registration
@cache_control(no_cache=True)
def registration(request):
    user_form = UserProfileForm()
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            phone_number = user_form.cleaned_data['phone_number']
            adress = user_form.cleaned_data['adress']
            user = User.objects.create_user(username=username,
                                            phone_number=phone_number,
                                            adress=adress)
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            info = 'Something is incorrect'
            return render(request,'registration.html',{'info':info})
    context = {'form': user_form}
    return render(request, 'registration.html', context)


# Profile view
@never_cache
@login_required(login_url='login')
@user_view
def profile_view(request, username):
    profile = User.objects.get(username=username)
    if profile.is_authenticated():
        return render(request, 'profile.html', {'profile': profile})
    else:
        return HttpResponse("Something wrongs!")


@login_required(login_url='login')
@api_view(['GET'])
@user_view
def serialized_profile_view(request, username):
    profile = User.objects.get(username=username)
    serializer = UserSerializer(profile)
    if profile.is_authenticated:
        return Response(serializer.data, status=status.HTTP_200_OK)


# Create the account
@login_required(login_url='login')
@user_view
def create_account(request, username):
    user = User.objects.get(username=username)
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
@login_required(login_url='logout_view')
@user_view
def account_view(request, username, account_holder):
    user = User.objects.get(username=username)
    account = Account.objects.get(user=user, account_holder=account_holder)
    outcomes = Charge.get_outcomes(account)
    incomes = Charge.get_incomes(account)
    months = Charge.get_by_month(account)
    return render(request, 'account.html', {'user': user,
                                            'account': account,
                                            'incomes': incomes,
                                            'outcomes': outcomes,
                                            'months': months})


@login_required(login_url='login')
@api_view(['GET'])
@user_view
def serialized_account_view(request, username, account_holder):
    user = User.objects.get(username=username)
    account = Account.objects.get(user=user, account_holder=account_holder)
    serializer = AccountSerializer(account)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Edit the account
@login_required(login_url='login')
@user_view
def edit_account(request, username, account_holder):
    user = User.objects.get(username=username)
    account = Account.objects.get(user=user, account_holder=account_holder)
    form = CreateAccount()
    if request.method == 'POST':
        form = CreateAccount(request.POST)
        if form.is_valid():
            new_account_holder = form.cleaned_data['account_holder']
            account.account_holder = new_account_holder
            account.save()
            return redirect('account_view', username, account_holder)
        else:
            return HttpResponse("Not valid")
    context = {'form': form}
    return render(request, 'edit_account.html', context, {'user': user, 'account': account})


# Delete the account
def delete_account(request, username, account_holder):
    user = User.objects.get(username=username)
    account = Account.objects.get(user=user, account_holder=account_holder)
    if request.method == 'POST':
        Account.object.filter(user=user, account_holder=account_holder).delete()
        return redirect('profile_view', username)
    else:
        return HttpResponse("Not valid")
    return render(request, 'edit_account.html', {'user': user, 'account': account})


# All user's accounts
@login_required(login_url='logout_view')
@user_view
def get_all_accounts(request, username, account_holder=0):
    user = User.objects.get(username=username)
    all_accounts = Account.objects.filter(user=user)
    print("All accounts: ")
    print(all_accounts)
    return render(request, 'all_accounts.html', {'all_accounts': all_accounts,
                                                 'user': user})


@login_required(login_url='login')
@api_view(['GET'])
@user_view
def serialized_get_all_accounts(request, username, account_holder=0):
    user = User.objects.get(username=username)
    all_accounts = Account.objects.filter(user=user)
    serializer = AccountSerializer(all_accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Charges of account
@login_required(login_url='logout_view')
@user_view
def charges(request, username, account_holder):
    user = User.objects.get(username=username)
    account = Account.objects.get(user=user, account_holder=account_holder)
    incomes = Charge.get_incomes(account)
    outcomes = Charge.get_outcomes(account)
    return render(request, 'charges.html', {'user': user,
                                            'account': account,
                                            'incomes': incomes,
                                            'outcomes': outcomes})


@login_required(login_url='login')
@api_view(['GET'])
@user_view
def serialized_charges(request, username, account_holder):
    user = User.objects.get(username=username)
    account = Account.objects.get(user=user, account_holder=account_holder)
    all_charges = Charge.objects.filter(account=account)
    serializer = ChargeSerializer(all_charges, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Create the charge
@login_required(login_url='logout_view')
@user_view
def create_charge(request, username, account_holder):
    user = User.objects.get(username=username)
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
@login_required(login_url='logout_view')
@user_view
def months(request, username, account_holder):
    try:
        user = User.objects.get(username=username)
        account = Account.objects.get(user=user, account_holder=account_holder)
        by_months = Charge.get_by_month(account)
    except ObjectDoesNotExist:
        print("Can't find")
    return render(request, 'months.html', {'user': user,'account': account, 'months': by_months})


@login_required(login_url='login')
@api_view(['GET'])
@user_view
def serialized_months(request, username, account_holder):
    user = User.objects.get(username=username)
    account = Account.objects.get(user=user, account_holder=account_holder)
    test = MonthStatCollection(account)
    return test.get(request)


# List of all users
@login_required(login_url='login')
def all_users(request):
    if request.user.is_superuser:
        users = User.objects.get_queryset()
        return render(request, 'all_users.html',{'users':users})
    else:
        return redirect('login')


# Edit user profile
@login_required(login_url='login')
@user_view
def edit_user(request, username):
    user = User.objects.get(username=username)
    form = UserProfileEdit()
    if request.method == 'POST':
        form = UserProfileEdit(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['userprofile']
            new_password = form.cleaned_data['password']
            new_phone_number = form.cleaned_data['phone_number']
            new_adress = form.cleaned_data['adress']
            if new_password is not 'NULL':
                user.set_password(new_password)
            if new_phone_number is not 'NULL':
                User.objects.filter(username=username).update(phone_number=new_phone_number)
            if new_adress is not 'NULL':
                User.objects.filter(username=username).update(adress=new_adress)
            if new_username is not 'NULL':
                User.objects.filter(username=username).update(username=new_username)
            return redirect('profile_view',new_username)
        else:
            return HttpResponse('Not valid')
    context = {'user': user, 'form': form}
    return render(request, 'edit_user.html', context)


@login_required(login_url='login')
def delete_user(request, username):
    if request.user.is_superuser:
        user = User.objects.get(username=username)
        if request.method == 'POST':
            User.objects.filter(username=username).delete()
            return redirect('all_users')
    else:
        return HttpResponse("Not valid")
    return render(request, 'delete_account.html', {'user': user})
