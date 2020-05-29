import requests
import os


def parse_date(date):
    """
    Method that check if date's day is lower that 15 (when the TMCs are updated).
    If is so, returns the previous month and its corresponding year. Otherwise,
    Returns the current month and its corresponding year
    """
    year = date.year
    month = date.month
    if date.day < 15:
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
    return year, month


def get_tmcs_by_date(date):
    """Gets the list of TMCs from SBIF API, for the given date"""
    year, month = parse_date(date)
    url = f"{os.environ.get('SBIF_URL')}/{year}/{month}/"

    params = {
        'apikey':  os.environ.get('SBIF_API_KEY'),
        'formato': 'json'
    }

    rsp = requests.get(url, params=params)

    if rsp.status_code != 200:
        raise Exception('Not valid response from SBIF')

    return rsp.json()['TMCs']
