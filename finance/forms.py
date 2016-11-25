from datetime import date
from django.forms import ModelForm
from finance.models import Charge, Account

class ChargeForm(ModelForm):

    class Meta:
        model = Charge
        fields = ['date','value']

    def clean(self):
        cleaned_data = super(ChargeForm, self).clean()
        date_charge = cleaned_data.get('date')
        value_charge = cleaned_data.get('value')
        today = date.today()
        if value_charge < 0:
            if date_charge > today:
                self.add_error('date',"Невозможно записать расход на будущее")
        return cleaned_data

    def save(self, user):
        obj = super(ChargeForm, self).save(commit=False)
        obj.account = user
        return obj.save()

class CreateAccount(ModelForm):

    class Meta:
        model = Account
        fields = ['account_holder']
