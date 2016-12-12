from rest_framework import views
from rest_framework.serializers import ModelSerializer, Serializer, CharField, IntegerField, DecimalField
from rest_framework.response import Response
from .models import Account, Charge


class AccountSerializer(ModelSerializer):

    class Meta:
        model = Account
        fields = ['account_holder', 'total']


class ChargeSerializer(ModelSerializer):
    account = AccountSerializer(source='account')

    class Meta:
        model = Charge
        fields = ['date', 'value', 'account']


class MonthStatSerializer(Serializer):

    month = CharField(max_length=16)
    amount = DecimalField(max_digits=8, decimal_places=2)


class MonthStatCollection(views.APIView):

    def __init__(self, account_holder):

        self.values = []

        account = Account.objects.get(account_holder=account_holder)
        by_months = Charge.get_by_month(account)

        for each in by_months:
            self.values.append({'month': each['month'], 'amount': each['c']})
            print(each)

    def get(self, request, format=None):
        serializer = MonthStatSerializer(self.values, many=True)
        return Response(serializer.data)
