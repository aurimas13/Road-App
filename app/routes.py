import os
import urllib
from datetime import datetime
from urllib import parse
from app.models import Weather, Traffic, BatchUpdate
from flask import request, Response
from app import app, db
from pprint import PrettyPrinter
from app.validate import validate_input
from marshmallow import ValidationError

pp = PrettyPrinter()

APP_BASE_URL = os.getenv("APP_BASE_URL")
PORT = os.getenv("PORT")


@app.route('/', methods=['GET'])
@app.route('/weather_conditions', methods=['POST', 'GET'])
def weather_conditions():
    """
    This is the method to show metrics of weather temperature, road temperature, wind speed of
    the road for a given period iand id or ids.
    """
    if request.method == 'GET':

        try:
            validate_input(request.url)
        except ValidationError:
            return Response(
                "Bad request was sent",
                status=400,
            )

        decoded_date_start = urllib.parse.unquote(request.args.get('period_start'))
        period_start = datetime.strptime(decoded_date_start, '%Y-%m-%d %X')
        id_list = request.args.get('ids').split(',')
        period_end = None
        query = db.session.query(Weather.oro_temperatura, Weather.vejo_greitis_vidut,
                                     Weather.dangos_temperatura, Weather.id)\
                .filter(Weather.id.in_(id_list))\
                .filter(Weather.surinkimo_data >= period_start)
        if request.args.get('period_end'):
            decoded_date_end = urllib.parse.unquote(request.args.get('period_end'))
            period_end = datetime.strptime(decoded_date_end, '%Y-%m-%d %X')
            query_results = query.filter(Weather.surinkimo_data <= period_end).all()
        else:
            query_results = query.all()

        result_dict = {}

        for row in query_results:
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
                'period_start': period_start,
                'period_end': period_end,
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

        return response_ls


@app.route('/traffic_intensity', methods=['GET'])
def traffic_intensity():
    """
    This is the method to show metrics of speed limits, number of Vehicles, avergae speed of vehicles
    in the road for a given period of an id or ids.
    """
    if request.method == 'GET':
        traffic_link = 'http://127.0.0.1:5000/traffic_intensity?ids=1805,3504,4398,23&period_start=2022-10-30%252012:00:00'
        decoded_date_start = urllib.parse.unquote(request.args.get('period_start'))
        period_start = datetime.strptime(decoded_date_start, '%Y-%m-%d %X')
        id_list = request.args.get('ids').split(',')
        period_end = None
        query = db.session.query(Traffic.winterSpeed, Traffic.summerSpeed, Traffic.numberOfVehicles,
                                 Traffic.averageSpeed, Traffic.id, Traffic.date) \
            .filter(Traffic.id.in_(id_list)) \
            .filter(Traffic.date >= period_start)
        if request.args.get('period_end'):
            decoded_date_end = urllib.parse.unquote(request.args.get('period_end'))
            period_end = datetime.strptime(decoded_date_end, '%Y-%m-%d %X')
            query_results = query.filter(Traffic.date <= period_end).all()
        else:
            query_results = query.all()

        result_dict = {}

        for row in query_results:
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
                'period_start': period_start,
                'period_end' : period_end,
                'statistics' : {
                    'averageSpeed_avg': item['averageSpeed'] / item['averageSpeed_cnt'] \
                        if item['averageSpeed_cnt'] != 0 else 0,
                    'numberOfVehicles_avg': item['numberOfVehicles'] / item['numberOfVehicles_cnt'] \
                        if item['numberOfVehicles_cnt'] != 0 else 0,
                }
            }
            response_ls.append(resp_per_id)
        print(response_ls)
        return response_ls
