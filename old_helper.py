import urllib

import requests
from urllib import parse
from app import app, db
from flask import request
from datetime import datetime


def fetch_data(url):
    response = requests.get(url)
    return response.json()


def decode_periods_and_ids(idx, period_from, period_until=None):
    decoded_period_start = urllib.parse.unquote(period_from)
    period_start = datetime.strptime(decoded_period_start, '%Y-%m-%d %X')
    decoded_period_end = urllib.parse.unquote(request.args.get('period_end')) if period_until != None else None
    period_end = datetime.strptime(decoded_period_end, '%Y-%m-%d %X') if period_until != None else None
    id_list = idx.split(',')
    return id_list, period_start, period_end


def extract_weather_data(query, period_from, period_until):
    result_dict = {}

    for row in query:
        if row['id'] not in result_dict:
            result_dict[row['id']] = {
                'dangos_temperatura': 0,
                'dangos_temperatura_cnt': 0,
                'oro_temperatura': 0,
                'oro_temperatura_cnt': 0,
                'vejo_greitis': 0,
                'vejo_greitis_cnt': 0,
            }

        dangos_temperatura = row['dangos_temperatura']
        if dangos_temperatura:
            result_dict[row['id']]['dangos_temperatura'] += dangos_temperatura
            result_dict[row['id']]['dangos_temperatura_cnt'] += 1

        oro_temperatura = row['oro_temperatura']
        if oro_temperatura:
            result_dict[row['id']]['oro_temperatura'] += oro_temperatura
            result_dict[row['id']]['oro_temperatura_cnt'] += 1

        vejo_greitis = row["vejo_greitis_vidut"]
        if vejo_greitis:
            result_dict[row['id']]['vejo_greitis'] += vejo_greitis
            result_dict[row['id']]['vejo_greitis_cnt'] += 1

    response_ls = []

    for key in result_dict:
        item = result_dict[key]
        resp_per_id = {
            'id': key,
            'period_start': period_from,
            'period_end': period_until,
            'statistics': {
                'dangos_temperatura_avg': item['dangos_temperatura'] / item['dangos_temperatura_cnt'] \
                    if item['dangos_temperatura_cnt'] != 0 else 0,
                'oro_temperatura_avg': item['oro_temperatura'] / item['oro_temperatura_cnt'] \
                    if item['oro_temperatura_cnt'] != 0 else 0,
                'vejo_greitis_avg': item['vejo_greitis'] / item['vejo_greitis_cnt'] \
                    if item['vejo_greitis_cnt'] != 0 else 0,
            }
        }
        response_ls.append(resp_per_id)

    return response_ls


def extract_traffic_data(query, period_from, period_until):
    result_dict = {}

    for row in query:
        if row['id'] not in result_dict:
            result_dict[row['id']] = {
                'averageSpeed': 0,
                'averageSpeed_cnt': 0,
                'numberOfVehicles': 0,
                'numberOfVehicles_cnt': 0,
            }

        averageSpeed = row['averageSpeed']
        if averageSpeed:
            result_dict[row['id']]['averageSpeed'] += averageSpeed
            result_dict[row['id']]['averageSpeed_cnt'] += 1

        numberOfVehicles = row["numberOfVehicles"]
        if numberOfVehicles:
            result_dict[row['id']]['numberOfVehicles'] += numberOfVehicles
            result_dict[row['id']]['numberOfVehicles_cnt'] += 1

    response_ls = []
    for key in result_dict:
        item = result_dict[key]
        resp_per_id = {
            'id': key,
            'period_start': period_from,
            'period_end': period_until,
            'statistics': {
                'averageSpeed_avg': item['averageSpeed'] / item['averageSpeed_cnt'] \
                    if item['averageSpeed_cnt'] != 0 else 0,
                'numberOfVehicles_avg': item['numberOfVehicles'] / item['numberOfVehicles_cnt'] \
                    if item['numberOfVehicles_cnt'] != 0 else 0,
            }
        }
        response_ls.append(resp_per_id)

    return response_ls
