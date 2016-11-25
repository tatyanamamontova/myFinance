from django.conf.urls import url
from finance.views import index, charges, create_account, get_all_accounts, account_view, months, create_charge

urlpatterns = [
    url(r'create/account', create_account, name='create_account'),
    url(r'account/(?P<account_holder>\w+)/charges', charges, name='all_charges'),
    url(r'account/(?P<account_holder>\w+)/charge', create_charge, name='new_charge'),
    url(r'account/(?P<account_holder>\w+)/months', months, name='months'),
    url(r'account/(?P<account_holder>\w+)', account_view, name='account_view'),
    url(r'allaccounts', get_all_accounts, name='all_accounts'),
    url(r'', index, name='index')
]
