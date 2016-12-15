from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from finance.views import serialized_charges, charges, create_account, serialized_account_view, account_view, \
    serialized_months, months, create_charge, login_view, registration, serialized_profile_view, profile_view, \
    logout_view, serialized_get_all_accounts, get_all_accounts, main_page, all_users, edit_account, delete_account,\
    edit_user,delete_user, charge_view, charge_edit, charge_delete, UserViewSet, AccountViewSet, ChargeViewSet, \
    csv_month

urlpatterns = [
    url(r'csv/(?P<username>\w+)/(?P<account_holder>\w+)', csv_month),
    url(r'^api/user/(?P<username>\w+)/account/(?P<account_holder>\w+)/charges/json$',
        ChargeViewSet.as_view({'get': 'list'})),
    url(r'^api/user/(?P<username>\w+)/accounts$', AccountViewSet.as_view({'get': 'list'})),

    # url(r'users/(?P<username>\w+)', UserViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),
    # url(r'users', csrf_exempt(UserViewSet.as_view({'get': 'list', 'post': 'create'}))),
    # url(r'accounts', AccountViewSet.as_view({'get': 'list'})),
    # url(r'allcharges', csrf_exempt(ChargeViewSet.as_view({'get': 'list', 'post': 'create'}))),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/charges/(?P<chargeid>\w+)/delete$', charge_delete,
        name='charge_delete'),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/charges/(?P<chargeid>\w+)/edit$', charge_edit,
        name='charge_edit'),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/charges/(?P<chargeid>\w+)/$', charge_view,
        name='charge_view'),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/charges/json$', serialized_charges),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/charges/$', charges, name='all_charges'),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/charge/$', create_charge, name='new_charge'),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/months/json$', serialized_months),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/months/$', months, name='months'),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/edit$', edit_account, name='edit_account'),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/delete$', delete_account, name='delete_account'),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/json$', serialized_account_view),
    url(r'user/(?P<username>\w+)/account/(?P<account_holder>\w+)/$', account_view, name='account_view'),
    url(r'create/user/$', registration, name='registration'),
    url(r'user/(?P<username>\w+)/create/account/$', create_account, name='create_account'),
    url(r'user/(?P<username>\w+)/accounts/json$', serialized_get_all_accounts),
    url(r'user/(?P<username>\w+)/accounts/$', get_all_accounts, name='get_all_accounts'),
    url(r'user/(?P<username>\w+)/edit/$', edit_user, name='edit_user'),
    url(r'user/(?P<username>\w+)/delete/$', delete_user, name='delete_user'),
    url(r'user/(?P<username>\w+)/json$', serialized_profile_view),
    url(r'user/(?P<username>\w+)/$', profile_view, name='profile_view'),
    url(r'all_users/',all_users, name='all_users'),
    url(r'^logout/$', logout_view, name='logout_view'),
    url(r'^login/$',login_view, name='login'),
    url(r'', main_page, name = 'main_page'),
]
