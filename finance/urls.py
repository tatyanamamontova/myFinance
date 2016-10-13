from django.conf.urls import url
from finance.views import hello_world

urlpatterns = [
    url(r'.*', hello_world),
]
