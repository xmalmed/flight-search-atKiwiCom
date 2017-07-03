#!/usr/bin/env python3
# Author Vojtech Kuban

import requests
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='Process flight parameters.')
parser.add_argument('--date', required=True, help='rrrr-mm-dd format')
parser.add_argument('--from', required=True, dest='start')
parser.add_argument('--to', required=True)
group_sort = parser.add_mutually_exclusive_group()
group_sort.add_argument('--cheapest', action='store_true', default=True)
group_sort.add_argument('--shortest', action='store_true', default=False)
group = parser.add_mutually_exclusive_group()
group.add_argument('--one-way', action='store_true', default=True)
group.add_argument('--return', type=int, dest='two_way', help='Number of nights.')

args = parser.parse_args()


def search_parameters(args) -> dict:
    """Prepare parameters for the API call."""
    date = datetime.strptime(args.date, '%Y-%m-%d').strftime('%d/%m/%Y')
    search_params = {
        'limit': '5',
        'flyFrom': args.start,
        'to': args.to,
        'dateFrom': date,
        'dateTo': date,
        'typeFlight': 'oneway',             # oneway/round
        'sort': 'price',                    # quality, price, date or duration
    }

    if args.shortest:
        search_params['sort'] = 'duration'

    if args.two_way is not None:
        search_params['typeFlight'] = 'round'
        search_params['daysInDestinationFrom'] = str(args.two_way)
        search_params['daysInDestinationTo'] = str(args.two_way)

    return search_params


def search_flight(params: dict) -> str:
    """Search for the best flight and return its booking_token."""
    flight = requests.get('https://api.skypicker.com/flights', params=params)
    return flight.json()['data'][0]['booking_token']


def book_flight(booking_token: str) -> str:
    """Book the flight according to booking_token and return PNR number."""
    param = {
        "currency": "EUR",
        "booking_token": booking_token,
        "passengers": [
            {
                "title": "Mr",
                "lastName": "Xxx",
                "firstName": "Yyy",
                "email": "xxx@goo.com",
                "documentID": "111111",
                "birthday": "1999-01-01",
            },
        ]
    }
    booking = requests.post('http://37.139.6.125:8080/booking', json=param)
    return booking.json()['pnr']


token = search_flight(search_parameters(args))
print(book_flight(token))
