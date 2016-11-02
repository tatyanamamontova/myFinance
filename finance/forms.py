from django.forms import Form, DecimalField, DateField
from django.utils import timezone


class ChargeForm(Form):

    value = DecimalField(
        label='Сумма',
        required=True
    )

    date = DateField(
        label='Дата',
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        now = timezone.now().date()
        if cleaned_data.get('value', 0) < 0 and cleaned_data.get('date') >= now:
            self.add_error('date', 'Нельзя заводить списание на будущее')
        return cleaned_data
