from django.conf.urls import url
from finance.views import hello_world
from finance.views import charges

urlpatterns = [
    url(r'charges', charges),
    url(r'.*', hello_world),
]
