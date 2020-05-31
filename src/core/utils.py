import requests
import os

from dateutil.relativedelta import relativedelta
from django.utils.translation import gettext_lazy as _


class SbifException(Exception):
    pass


def parse_date(date):
    """
    Method that check if date's day is lower that 15 (when the TMCs are updated).
    If is so, returns the previous month and its corresponding year. Otherwise,
    Returns the current month and its corresponding year
    """
    if date.day < 15:
        date -= relativedelta(months=1)
    return date.year, date.month


def get_tmcs_by_date(date):
    """Gets the list of TMCs from SBIF API, for the given date"""
    year, month = parse_date(date)
    url = f"{os.environ.get('SBIF_URL')}/{year}/{month}/"

    params = {
        'apikey':  os.environ.get('SBIF_API_KEY'),
        'formato': 'json'
    }

    rsp = requests.get(url, params=params, timeout=float(os.getenv('SBIF_TIMEOUT_SECS', 10)))

    if rsp.status_code != 200:
        print(rsp.content)
        if rsp.status_code == 404:
            raise SbifException(_('No data found in SBIF for the given date'))
        raise

    return rsp.json()['TMCs']
