from datetime import date
from requests.exceptions import Timeout

from django import forms
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

from .utils import get_tmcs_by_date, SbifException
from .models import Operation


def validate_max_date(value):
    max_date = date.today() + relativedelta(months=1, day=14)

    if value > max_date:
        raise ValidationError(
            _('Max date allowed is {}'.format(max_date)),
            params={'value': value},
        )


class LoanForm(forms.Form):
    term = forms.IntegerField(label=_('Term in days'), validators=[MinValueValidator(0)])
    amount = forms.FloatField(label=_('Amount in UF'), validators=[MinValueValidator(0.0)])
    date = forms.DateField(
        label=_('Date'),
        initial=date.today,
        validators=[validate_max_date],
    )

    def find_tmc(self):
        data = self.cleaned_data
        code = Operation.objects.find_code(data['term'], data['amount'])

        try:
            tmcs = get_tmcs_by_date(data['date'])
        except SbifException as e:
            return str(e)
        except Timeout:
            return _('SBIF service timed out')
        except Exception:
            return _('A problem occurred with the SBIF service')

        for tmc in tmcs:
            if tmc['Tipo'] == code:
                return _('TMC value: {}%').format(tmc['Valor'])

        return _('TMC was not found for the given parameters')
