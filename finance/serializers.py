from rest_framework.serializers import ModelSerializer
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