from datetime import date
from unittest import mock

from django.test import TestCase
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

from .models import Operation
from . import utils
from .forms import LoanForm


class ModelsTest(TestCase):
    """Test the model's methods"""

    def setUp(self):
        Operation.objects.create(
            code=1,
            title='A title',
            subtitle='A subtitle',
            term_min=5,
            term_max=10,
            amount_min=500.0,
            amount_max=1000.0
        )

    def test_find_code(self):
        self.assertEqual('1', Operation.objects.find_code(5, 1000))
        self.assertNotEqual('1', Operation.objects.find_code(4, 1000))
        self.assertEqual('1', Operation.objects.find_code(9, 1000))
        self.assertNotEqual('1', Operation.objects.find_code(10, 1000))
        self.assertNotEqual('1', Operation.objects.find_code(5, 1000.1))
        self.assertEqual('1', Operation.objects.find_code(5, 500.1))
        self.assertNotEqual('1', Operation.objects.find_code(5, 500.0))


def mocked_parse_date(*args, **kwargs):
    if args[0] == 1:
        return 2020, 5
    else:
        return 2020, 6


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def content(self):
            return self.json_data

    if args[0] == 'http://url.com/2020/5/':
        return MockResponse({"TMCs": [1]}, 200)

    return MockResponse(None, 404)


class UtilsTest(TestCase):
    """Test methods in utils module"""

    def test_parse_date(self):
        self.assertEqual((2020, 1), utils.parse_date(date(2020, 1, 15)))
        self.assertEqual((2019, 12), utils.parse_date(date(2020, 1, 14)))

    @mock.patch('core.utils.parse_date', side_effect=mocked_parse_date)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_tmcs_by_date(self, MockClass1, MockClass2):
        with mock.patch.dict('os.environ', {'SBIF_URL': 'http://url.com', 'SBIF_API_KEY': '1234'}, clear=True):
            self.assertEqual([1], utils.get_tmcs_by_date(1))
            with self.assertRaises(utils.SbifException):
                utils.get_tmcs_by_date(2)


class FormsTest(TestCase):
    """Test form's methods"""
    def test_clean_date(self):
        test_date = date.today() + relativedelta(months=1, day=14)
        form = LoanForm(data={'term': 5, 'amount': 500, 'date': test_date})
        self.assertTrue(form.is_valid())
        self.assertEqual(test_date, form.cleaned_data.get('date', None))

        test_date = date.today() + relativedelta(months=1, day=15)
        form = LoanForm(data={'term': 5, 'amount': 500, 'date': test_date})
        self.assertFalse(form.is_valid())
        self.assertEqual(None, form.cleaned_data.get('date', None))
