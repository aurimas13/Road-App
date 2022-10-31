import os
import urllib
from datetime import datetime
from urllib import parse
from app.models import Weather, Traffic, BatchUpdate
from flask import request, Response
from app import app, db
from pprint import PrettyPrinter
from app.validate import validate_input
from app.helper import decode_periods_and_ids, extract_weather_data, extract_traffic_data
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

    :return: list of dictionaries or dictionary
    """
    if request.method == 'GET':

        try:
            validate_input(request.url)
        except ValidationError:
            return Response(
                "Bad request was sent",
                status=400,
            )

        if request.args.get('period_end'):
            decoded_values = decode_periods_and_ids(request.args.get('ids'), request.args.get('period_start'), request.args.get('period_end'),)
            query = db.session.query(Weather.oro_temperatura, Weather.vejo_greitis_vidut,
                                     Weather.dangos_temperatura, Weather.id) \
                .filter(Weather.id.in_(decoded_values[0])) \
                .filter(Weather.surinkimo_data >= decoded_values[1]) \
                .filter(Weather.surinkimo_data <= decoded_values[2]).all()
        else:
            decoded_values = decode_periods_and_ids(request.args.get('ids'), request.args.get('period_start'), request.args.get('period_end'),)
            query = db.session.query(Weather.oro_temperatura, Weather.vejo_greitis_vidut,
                                     Weather.dangos_temperatura, Weather.id) \
                .filter(Weather.id.in_(decoded_values[0])) \
                .filter(Weather.surinkimo_data >= decoded_values[1]).all()

        weather_conditions_gotten_data = extract_weather_data(query, decoded_values[1], decoded_values[2])
        print(type(weather_conditions_gotten_data))
        return weather_conditions_gotten_data


@app.route('/traffic_intensity', methods=['GET'])
def traffic_intensity():
    """
    This is the method to show average metrics of speed limits, number of Vehicles, average speed of vehicles
    in the road for a given period of an id or ids.

    :return: list of dictionaries or dictionary
    """
    if request.method == 'GET':
        if request.args.get('period_end'):
            decoded_values = decode_periods_and_ids(request.args.get('ids'), request.args.get('period_start'), request.args.get('period_end'),)
            query = db.session.query(Traffic.winterSpeed, Traffic.summerSpeed, Traffic.numberOfVehicles,
                                     Traffic.averageSpeed, Traffic.id, Traffic.date) \
                .filter(Traffic.id.in_(decoded_values[0])) \
                .filter(Traffic.date >= decoded_values[1]) \
                .filter(Traffic.date <= decoded_values[2]).all()
            pp.pprint(type(decoded_values))
        else:
            decoded_values = decode_periods_and_ids(request.args.get('ids'), request.args.get('period_start'), request.args.get('period_end'),)
            query = db.session.query(Traffic.winterSpeed, Traffic.summerSpeed, Traffic.numberOfVehicles,
                                     Traffic.averageSpeed, Traffic.id, Traffic.date) \
                .filter(Traffic.id.in_(decoded_values[0])) \
                .filter(Traffic.date >= decoded_values[1]).all()
        traffic_intensity_gotten_data = extract_traffic_data(query, decoded_values[1], decoded_values[2])
        return traffic_intensity_gotten_data
