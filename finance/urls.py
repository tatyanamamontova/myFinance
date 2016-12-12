from django.conf.urls import url
from finance.views import charges, create_account, get_all_accounts, account_view, months, create_charge, \
    serialized_get_all_accounts, serialized_account_view, serialized_months, login_view, logout_view

urlpatterns = [
    url(r'login', login_view, name='login'),
    url(r'logout', logout_view, name='logout'),
    url(r'create/account', create_account, name='create_account'),
    url(r'account/(?P<account_holder>\w+)/charges', charges, name='all_charges'),
    url(r'account/(?P<account_holder>\w+)/charge', create_charge, name='new_charge'),
    url(r'account/(?P<account_holder>\w+)/months.json$', serialized_months),
    url(r'account/(?P<account_holder>\w+)/months', months, name='months'),
    url(r'account/(?P<account_holder>\w+).json$', serialized_account_view),
    url(r'account/(?P<account_holder>\w+)', account_view, name='account_view'),
    url(r'json', serialized_get_all_accounts),
    url(r'', get_all_accounts, name='all_accounts'),
]
