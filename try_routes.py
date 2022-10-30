import itertools
import os

import werkzeug
import sys
from app.models import Weather, Traffic, BatchUpdate
from flask import render_template, flash, redirect, url_for, request, Response, jsonify
from app import app, db
from pprint import PrettyPrinter
from itertools import groupby
from operator import itemgetter

from sqlalchemy.sql import func
import json
import urllib.parse

pp = PrettyPrinter()
from fetch import *

APP_BASE_URL = os.getenv("APP_BASE_URL")
PORT = os.getenv("PORT")


@app.route('/', methods=['GET'])
@app.route('/weather_conditions', methods=['POST', 'GET'])
def weather_conditions():
    """
    This is the method to show metrics of weather temperature, road temperature, wind speed,
    visibility of the road for a given period in a road of an id or ids.
    """
    if request.method == 'GET':

        weather_link = 'http://127.0.0.1:5000/weather_conditions?ids=310,308,363,1208&date_from=2022-10-30%252012:00:00'
        decoded_date = urllib.parse.unquote(request.args.get('date_from'))
        period = datetime.strptime(decoded_date, '%Y-%m-%d %X')
        id_list = request.args.get('ids').split(',')
        query = db.session.query(Weather.oro_temperatura, Weather.vejo_greitis_vidut,
                                 Weather.dangos_temperatura, Weather.id)\
            .filter(Weather.id.in_(id_list))\
            .filter(Weather.surinkimo_data >= period).all()

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
                    'period_start': 0,
                    'period_end': None,
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
                'period_start': 0,
                'period_end': None,
                'statistics': {
                    'dangos_temperatura_avg': item['dangos_temperatura'] / item['dangos_temperatura_cnt']\
                        if item['dangos_temperatura_cnt'] != 0 else 0,
                    'oro_temperatura_avg': item['oro_temperatura'] / item['oro_temperatura_cnt']\
                        if item['oro_temperatura_cnt'] != 0 else 0,
                    'vejo_greitis_avg': item['vejo_greitis'] / item['vejo_greitis_cnt']\
                        if item['vejo_greitis_cnt'] != 0 else 0,
                }
            }
            response_ls.append(resp_per_id)
        print(response_ls)
        return response_ls


@app.route('/traffic_intensity', methods=['GET'])
def traffic_intensity():
    """
    This is the method to show metrics of speed limits, number of Vehicles, avergae speed of vehicles
    in the road for a given period of an id or ids.
    """
    if request.method == 'GET':
        traffic_link = 'http://127.0.0.1:5000/traffic_intensity?ids=1805,3504,4398,23&date_from=2022-10-30%252012:00:00'
        decoded_date = urllib.parse.unquote(request.args.get('date_from'))
        period = datetime.strptime(decoded_date, '%Y-%m-%d %X')
        id_list = request.args.get('ids').split(',')
        query = db.session.query(Traffic.winterSpeed, Traffic.summerSpeed, Traffic.numberOfVehicles,\
                                 Traffic.averageSpeed, Traffic.id, Traffic.date)\
            .filter(Traffic.id.in_(id_list))\
            .filter(Traffic.date >= period).all()

        result_dict = {}

        for row in query:
            if row['id'] not in result_dict:
                result_dict[row['id']] = {
                    'winterSpeed': 0,
                    'winterSpeed_cnt': 0,
                    'summerSpeed': 0,
                    'summerSpeed_cnt': 0,
                    'averageSpeed': 0,
                    'averageSpeed_cnt': 0,
                    'numberOfVehicles': 0,
                    'numberOfVehicles_cnt': 0,
                    'period_start' : 0,
                    'period_end' : None,
                }

            winterSpeed = row['winterSpeed']
            if winterSpeed:
                result_dict[row['id']]['winterSpeed'] += winterSpeed
                result_dict[row['id']]['winterSpeed_cnt'] += 1

            summerSpeed = row['summerSpeed']
            if summerSpeed:
                result_dict[row['id']]['summerSpeed'] += summerSpeed
                result_dict[row['id']]['summerSpeed_cnt'] += 1

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
                'period_start': 0,
                'period_end' : None,
                'statistics' : {
                    'winterSpeed_avg': item['winterSpeed'] / item['winterSpeed_cnt'] \
                        if item['winterSpeed_cnt'] != 0 else 0,
                    'summerSpeed_avg': item['summerSpeed'] / item['summerSpeed_cnt'] \
                        if item['summerSpeed_cnt'] != 0 else 0,
                    'averageSpeed_avg': item['averageSpeed'] / item['averageSpeed_cnt'] \
                        if item['averageSpeed_cnt'] != 0 else 0,
                    'numberOfVehicles_avg': item['numberOfVehicles'] / item['numberOfVehicles_cnt'] \
                        if item['numberOfVehicles_cnt'] != 0 else 0,
                }
            }
            response_ls.append(resp_per_id)
        print(response_ls)
        return response_ls
