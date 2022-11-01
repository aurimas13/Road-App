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


# def extract_traffic_data_old(query, period_from, period_until):
#     """
#     Method to extract traffic intensity numerical information per query.

#     :param query: list
#     :param period_from: datetime.datetime
#     :param period_until: datetime.datetime
#     :return: list of dictionaries or dictionary
#     """
#     result_dict = {}

#     for row in query:
#         if row['id'] not in result_dict:
#             result_dict[row['id']] = {
#                 'averageSpeed': 0,
#                 'averageSpeed_cnt': 0,
#                 'numberOfVehicles': 0,
#                 'numberOfVehicles_cnt': 0,
#             }

#         averageSpeed = row['averageSpeed']
#         if averageSpeed:
#             result_dict[row['id']]['averageSpeed'] += averageSpeed
#             result_dict[row['id']]['averageSpeed_cnt'] += 1

#         numberOfVehicles = row["numberOfVehicles"]
#         if numberOfVehicles:
#             result_dict[row['id']]['numberOfVehicles'] += numberOfVehicles
#             result_dict[row['id']]['numberOfVehicles_cnt'] += 1

#     response_ls = []
#     for key in result_dict:
#         item = result_dict[key]
#         resp_per_id = {
#             'id': key,
#             'period_start': period_from,
#             'period_end': period_until,
#             'statistics': {
#                 'averageSpeed_avg': float("{:.1f}".format(item['averageSpeed'] / item['averageSpeed_cnt'])) \
#                     if item['averageSpeed_cnt'] != 0 else 0,
#                 'numberOfVehicles_avg': float("{:.1f}".format(item['numberOfVehicles'] / item['numberOfVehicles_cnt'])) \
#                     if item['numberOfVehicles_cnt'] != 0 else 0,
#             }
#         }
#         response_ls.append(resp_per_id)

#     return response_ls


# def extract_weather_data_old(query, period_from, period_until):
#     """
#     Method to extract weather condition numerical information per query.

#     :param query: list of tuples
#     :param period_from: datetime.datetime
#     :param period_until: datetime.datetime
#     :return: list of dictionaries
#     """
#     result_dict = {}

#     for row in query:
#         if row['id'] not in result_dict:
#             result_dict[row['id']] = {
#                 'dangos_temperatura': 0,
#                 'dangos_temperatura_cnt': 0,
#                 'oro_temperatura': 0,
#                 'oro_temperatura_cnt': 0,
#                 'vejo_greitis_vidut': 0,
#                 'vejo_greitis_vidut_cnt': 0,
#                 'vejo_greitis_maks': 0,
#                 'vejo_greitis_maks_cnt': 0,
#                 'krituliu_kiekis': 0,
#                 'krituliu_kiekis_cnt': 0,
#                 'rasos_taskas': 0,
#                 'rasos_taskas_cnt': 0,
#                 'sukibimo_koeficientas': 0,
#                 'sukibimo_koeficientas_cnt': 0,
#                 'konstrukcijos_temp_007': 0,
#                 'konstrukcijos_temp_007_cnt': 0,
#                 'konstrukcijos_temp_020': 0,
#                 'konstrukcijos_temp_020_cnt': 0,
#                 'konstrukcijos_temp_050': 0,
#                 'konstrukcijos_temp_050_cnt': 0,
#                 'konstrukcijos_temp_080': 0,
#                 'konstrukcijos_temp_080_cnt': 0,
#                 'konstrukcijos_temp_110': 0,
#                 'konstrukcijos_temp_110_cnt': 0,
#                 'konstrukcijos_temp_130': 0,
#                 'konstrukcijos_temp_130_cnt': 0,
#                 'konstrukcijos_temp_140': 0,
#                 'konstrukcijos_temp_140_cnt': 0,
#                 'konstrukcijos_temp_170': 0,
#                 'konstrukcijos_temp_170_cnt': 0,
#                 'konstrukcijos_temp_200': 0,
#                 'konstrukcijos_temp_200_cnt': 0,
#             }

#         dangos_temperatura = row['dangos_temperatura']
#         if dangos_temperatura:
#             result_dict[row['id']]['dangos_temperatura'] += dangos_temperatura
#             result_dict[row['id']]['dangos_temperatura_cnt'] += 1

#         oro_temperatura = row['oro_temperatura']
#         if oro_temperatura:
#             result_dict[row['id']]['oro_temperatura'] += oro_temperatura
#             result_dict[row['id']]['oro_temperatura_cnt'] += 1

#         vejo_greitis_vidut = row["vejo_greitis_vidut"]
#         if vejo_greitis_vidut:
#             result_dict[row['id']]['vejo_greitis_vidut'] += vejo_greitis_vidut
#             result_dict[row['id']]['vejo_greitis_vidut_cnt'] += 1

#         vejo_greitis_maks = row["vejo_greitis_maks"]
#         if vejo_greitis_maks:
#             result_dict[row['id']]['vejo_greitis_maks'] += vejo_greitis_maks
#             result_dict[row['id']]['vejo_greitis_maks_cnt'] += 1

#         krituliu_kiekis = row["krituliu_kiekis"]
#         if krituliu_kiekis:
#             result_dict[row['id']]['krituliu_kiekis'] += krituliu_kiekis
#             result_dict[row['id']]['krituliu_kiekis_cnt'] += 1

#         rasos_taskas = row["rasos_taskas"]
#         if rasos_taskas:
#             result_dict[row['id']]['rasos_taskas'] += rasos_taskas
#             result_dict[row['id']]['rasos_taskas_cnt'] += 1

#         sukibimo_koeficientas = row["sukibimo_koeficientas"]
#         if sukibimo_koeficientas:
#             result_dict[row['id']]['sukibimo_koeficientas'] += sukibimo_koeficientas
#             result_dict[row['id']]['sukibimo_koeficientas_cnt'] += 1

#         konstrukcijos_temp_007 = row["konstrukcijos_temp_007"]
#         if konstrukcijos_temp_007:
#             result_dict[row['id']]['konstrukcijos_temp_007'] += konstrukcijos_temp_007
#             result_dict[row['id']]['konstrukcijos_temp_007_cnt'] += 1

#         konstrukcijos_temp_020 = row["konstrukcijos_temp_020"]
#         if konstrukcijos_temp_020:
#             result_dict[row['id']]['konstrukcijos_temp_020'] += konstrukcijos_temp_020
#             result_dict[row['id']]['konstrukcijos_temp_020_cnt'] += 1

#         konstrukcijos_temp_050 = row["konstrukcijos_temp_050"]
#         if konstrukcijos_temp_050:
#             result_dict[row['id']]['konstrukcijos_temp_050'] += konstrukcijos_temp_050
#             result_dict[row['id']]['konstrukcijos_temp_050_cnt'] += 1

#         konstrukcijos_temp_080 = row["konstrukcijos_temp_080"]
#         if konstrukcijos_temp_080:
#             result_dict[row['id']]['konstrukcijos_temp_080'] += konstrukcijos_temp_080
#             result_dict[row['id']]['konstrukcijos_temp_080_cnt'] += 1

#         konstrukcijos_temp_110 = row["konstrukcijos_temp_110"]
#         if konstrukcijos_temp_110:
#             result_dict[row['id']]['konstrukcijos_temp_110'] += konstrukcijos_temp_110
#             result_dict[row['id']]['konstrukcijos_temp_110_cnt'] += 1

#         konstrukcijos_temp_130 = row["konstrukcijos_temp_130"]
#         if konstrukcijos_temp_130:
#             result_dict[row['id']]['konstrukcijos_temp_130'] += konstrukcijos_temp_130
#             result_dict[row['id']]['konstrukcijos_temp_130_cnt'] += 1

#         konstrukcijos_temp_140 = row["konstrukcijos_temp_140"]
#         if konstrukcijos_temp_140:
#             result_dict[row['id']]['konstrukcijos_temp_140'] += konstrukcijos_temp_140
#             result_dict[row['id']]['konstrukcijos_temp_140_cnt'] += 1

#         konstrukcijos_temp_170 = row["konstrukcijos_temp_170"]
#         if konstrukcijos_temp_170:
#             result_dict[row['id']]['konstrukcijos_temp_170'] += konstrukcijos_temp_170
#             result_dict[row['id']]['konstrukcijos_temp_170_cnt'] += 1

#         konstrukcijos_temp_200 = row["konstrukcijos_temp_200"]
#         if konstrukcijos_temp_200:
#             result_dict[row['id']]['konstrukcijos_temp_200'] += konstrukcijos_temp_200
#             result_dict[row['id']]['konstrukcijos_temp_200_cnt'] += 1

#     response_ls = []

#     for key in result_dict:
#         item = result_dict[key]
#         resp_per_id = {
#             'id': key,
#             'period_start': period_from,
#             'period_end': period_until,
#             'statistics': {
#                 'dangos_temperatura_avg': float(
#                     "{:.1f}".format(item['dangos_temperatura'] / item['dangos_temperatura_cnt'])) \
#                     if item['dangos_temperatura_cnt'] != 0 else 0,
#                 'oro_temperatura_avg': float("{:.1f}".format(item['oro_temperatura'] / item['oro_temperatura_cnt'])) \
#                     if item['oro_temperatura_cnt'] != 0 else 0,
#                 'vejo_greitis_vidut_avg': float(
#                     "{:.1f}".format(item['vejo_greitis_vidut'] / item['vejo_greitis_vidut_cnt'])) \
#                     if item['vejo_greitis_vidut_cnt'] != 0 else 0,
#                 'vejo_greitis_maks_avg': float(
#                     "{:.1f}".format(item['vejo_greitis_maks'] / item['vejo_greitis_maks_cnt'])) \
#                     if item['vejo_greitis_maks_cnt'] != 0 else 0,
#                 'krituliu_kiekis_avg': float("{:.1f}".format(item['krituliu_kiekis'] / item['krituliu_kiekis_cnt'])) \
#                     if item['krituliu_kiekis_cnt'] != 0 else 0,
#                 'rasos_taskas': float("{:.1f}".format(item['rasos_taskas'] / item['rasos_taskas_cnt'])) \
#                     if item['rasos_taskas_cnt'] != 0 else 0,
#                 'sukibimo_koeficientas': float(
#                     "{:.1f}".format(item['sukibimo_koeficientas'] / item['sukibimo_koeficientas_cnt'])) \
#                     if item['sukibimo_koeficientas_cnt'] != 0 else 0,
#                 'konstrukcijos_temp_007_avg': float(
#                     "{:.1f}".format(item['konstrukcijos_temp_007'] / item['konstrukcijos_temp_007_cnt'])) \
#                     if item['konstrukcijos_temp_007_cnt'] != 0 else 0,
#                 'konstrukcijos_temp_020_avg': float(
#                     "{:.1f}".format(item['konstrukcijos_temp_020'] / item['konstrukcijos_temp_020_cnt'])) \
#                     if item['konstrukcijos_temp_020_cnt'] != 0 else 0,
#                 'konstrukcijos_temp_050_avg': float(
#                     "{:.1f}".format(item['konstrukcijos_temp_050'] / item['konstrukcijos_temp_050_cnt'])) \
#                     if item['konstrukcijos_temp_050_cnt'] != 0 else 0,
#                 'konstrukcijos_temp_080_avg': float(
#                     "{:.1f}".format(item['konstrukcijos_temp_080'] / item['konstrukcijos_temp_080_cnt'])) \
#                     if item['konstrukcijos_temp_080_cnt'] != 0 else 0,
#                 'konstrukcijos_temp_110_avg': float(
#                     "{:.1f}".format(item['konstrukcijos_temp_110'] / item['konstrukcijos_temp_110_cnt'])) \
#                     if item['konstrukcijos_temp_110_cnt'] != 0 else 0,
#                 'konstrukcijos_temp_130_avg': float(
#                     "{:.1f}".format(item['konstrukcijos_temp_130'] / item['konstrukcijos_temp_130_cnt'])) \
#                     if item['konstrukcijos_temp_130_cnt'] != 0 else 0,
#                 'konstrukcijos_temp_140_avg': float(
#                     "{:.1f}".format(item['konstrukcijos_temp_140'] / item['konstrukcijos_temp_140_cnt'])) \
#                     if item['konstrukcijos_temp_140_cnt'] != 0 else 0,
#                 'konstrukcijos_temp_170_avg': float(
#                     "{:.1f}".format(item['konstrukcijos_temp_170'] / item['konstrukcijos_temp_170_cnt'])) \
#                     if item['konstrukcijos_temp_170_cnt'] != 0 else 0,
#                 'konstrukcijos_temp_200_avg': float(
#                     "{:.1f}".format(item['konstrukcijos_temp_200'] / item['konstrukcijos_temp_200_cnt'])) \
#                     if item['konstrukcijos_temp_200_cnt'] != 0 else 0,
#             }
#         }
#         response_ls.append(resp_per_id)

#     return response_ls
