from django.conf.urls import url
from finance.views import charges, create_account, account_view, months, create_charge,login_view, registration, \
    profile_view, logout_view, get_all_accounts

urlpatterns = [
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/charges/$', charges, name='all_charges'),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/charge/$', create_charge, name='new_charge'),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/months/$', months, name='months'),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/$', account_view, name='account_view'),
    url(r'create/user/$', registration, name='registration'),
    url(r'user/(?P<username>\w+)/create/account/$', create_account, name='create_account'),
    url(r'user/(?P<username>\w+)/accounts/$', get_all_accounts, name='get_all_accounts'),
    url(r'user/(?P<username>\w+)/$', profile_view, name='profile_view'),
    url(r'^logout/$', logout_view, name='logout_view'),
    url(r'', login_view, name='login'),


]
