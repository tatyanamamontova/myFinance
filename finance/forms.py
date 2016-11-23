# from django.forms import Form, DecimalField, DateField
# from django.utils import timezone
#
#
# class ChargeForm(Form):
#
#     value = DecimalField(
#         label='Summ',
#         required=True
#     )
#
#     date = DateField(
#         label='Date',
#         required=True
#     )
#
#     def clean(self):
#         cleaned_data = super().clean()
#         now = timezone.now().date()
#         if cleaned_data.get('value', 0) < 0 and cleaned_data.get('date') >= now:
#             self.add_error('date', "You can't do it")
#         return cleaned_data
from datetime import date
from django.forms import ModelForm, fields
from finance.models import Charge, Account


class ChargeForm(ModelForm):

    class Meta:
        model = Charge
        fields = ['date','value']

    def clean(self):
        cleaned_data = super(ChargeForm, self).clean()
        date_charge = cleaned_data.get('date')
        value_charge = cleaned_data.get('value')
        today =  date.today()
        if  value_charge < 0:
            if date_charge > today:
                self.add_error('date',"Impossible to make a write-off")
                self.add_error('value',"Impossible to make a write-off")
        return cleaned_data

    def save(self, user):
        obj = super(ChargeForm, self).save(commit=False)
        obj.account = user
        return obj.save()

class AccountForm(ModelForm):

    class Meta:
        model = Account
        fields = ['account_id','income','outcome']