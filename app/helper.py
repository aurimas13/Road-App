import urllib

import pytz
import requests
from urllib import parse
from flask import request
from datetime import datetime


def fetch_data(url):
    """
    Method to fetch data from an API request.

    :param url: string
    :return: list of dictionaries
    """
    response = requests.get(url)
    return response.json()


def change_date_to_utc(date):
    """
    Method to convert time  to UTC time.

    :param date: string
    :return: datetime.datetime
    """

    local_timezone = pytz.timezone("Europe/Vilnius")
    result_date = datetime.strptime(date, '%Y-%m-%d %H:%M')
    local_date = local_timezone.localize(result_date)
    utc_date = local_date.astimezone(pytz.utc)
    return utc_date


def decode_periods_and_ids(idx, period_from, period_until=None):
    """
    Method to decode parameters from API request and convert them to readable values.

    :param idx: list of tuples
    :param period_from: datetime.datetime
    :param period_until: datetime.datetime
    :return: tuple
    """

    decoded_period_start = urllib.parse.unquote(period_from)
    period_start = datetime.strptime(decoded_period_start, '%Y-%m-%d %X')
    decoded_period_end = urllib.parse.unquote(request.args.get('period_end')) if period_until is not None else None
    period_end = datetime.strptime(decoded_period_end, '%Y-%m-%d %X') if period_until is not None else None
    id_list = idx.split(',')
    return id_list, period_start, period_end


def get_sum_attribute_values(data, attributes):
    """
    Method to create a dictionary of the sums and counts of valid attribute values (not null) per id. 

    :param data: list of dicts
    :param attributes: list
    :return: dictionary
    """
    result_dict = {}
    for row in data:
        # Initialize empty result_dict
        if row['id'] not in result_dict:
            result_dict[row['id']] = {}
            for key in attributes:
                result_dict[row['id']][key] = 0
                result_dict[row['id']][f"{key}_cnt"] = 0

        # Find sum of attributes to later find average
        for key in attributes:
            if row[key]:
                # Find sum of attributes to later find average
                result_dict[row['id']][key] += row[key]
                result_dict[row['id']][f"{key}_cnt"] += 1
    
    return result_dict


def get_response_values(data, attributes, period_from, period_until):
    """
    Method to create the response to the query. The response calculates the average
    values per attribute provided

    :param data: dict
    :param attributes: list
    :param period_from: datetime.datetime
    :param period_until: datetime.datetime
    :return: list of dictionaries
    """
    response_ls = []

    for key in data:
        item = data[key]
        resp_per_id = {
            'id': key,
            'period_start': period_from,
            'period_end': period_until,
            'statistics': {}
        }

        # Get average per attribute
        for key in attributes:
            if item[f"{key}_cnt"] != 0:
                resp_per_id['statistics'][f"{key}_avg"] = float("{:.1f}".format(item[key] / item[f"{key}_cnt"]))
            else:
                resp_per_id['statistics'][f"{key}_avg"] = 0.0
        response_ls.append(resp_per_id)

    return response_ls


def extract_traffic_data(query, period_from, period_until):
    """
    Method to extract traffic intensity numerical information per query.

    :param query: list
    :param period_from: datetime.datetime
    :param period_until: datetime.datetime
    :return: list of dictionaries or dictionary
    """
    keys = [
        'summerSpeed',
        'winterSpeed',
        'averageSpeed',
        'numberOfVehicles'
    ]
    # Calculate the sum and counts of all valid values for keys
    result_dict = get_sum_attribute_values(query, keys)
    
    # Calculate respose with average values per attribute
    response_ls = get_response_values(result_dict, keys, period_from, period_until)

    return response_ls


def extract_weather_data(query, period_from, period_until):
    """
    Method to extract weather condition numerical information per query.

    :param query: list of tuples
    :param period_from: datetime.datetime
    :param period_until: datetime.datetime
    :return: list of dictionaries
    """
    keys = [
        'dangos_temperatura',
        'oro_temperatura',
        'vejo_greitis_vidut',
        'vejo_greitis_maks',
        'krituliu_kiekis',
        'rasos_taskas',
        'sukibimo_koeficientas',
        'konstrukcijos_temp_007',
        'konstrukcijos_temp_020',
        'konstrukcijos_temp_050',
        'konstrukcijos_temp_080',
        'konstrukcijos_temp_110',
        'konstrukcijos_temp_130',
        'konstrukcijos_temp_140',
        'konstrukcijos_temp_170',
        'konstrukcijos_temp_200',
    ]
    # Calculate the sum and counts of all valid values for keys
    result_dict = get_sum_attribute_values(query, keys)
    
    # Calculate respose with average values per attribute
    response_ls = get_response_values(result_dict, keys, period_from, period_until)

    return response_ls
