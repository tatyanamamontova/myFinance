from django.conf.urls import url
from finance.views import index, charges

urlpatterns = [
    url(r'charges', charges, name='charges'),
    url(r'', index, name='index')
]
