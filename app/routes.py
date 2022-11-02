import os
import json

from flask import request, Response
from marshmallow import ValidationError

from app.models import Weather, Traffic
from app import app, db
from app.data_validation import validate_input
from app.helper import decode_periods_and_ids, extract_weather_data, extract_traffic_data

APP_BASE_URL = os.getenv("APP_BASE_URL")
PORT = os.getenv("PORT")


@app.route('/', methods=['GET'])
def default():
    return Response(
        json.dumps(
            {"message": "Use one of the two endpoints: weather_conditions or traffic intensity to get results!"}),
        status=200,
    )


@app.route('/weather_conditions', methods=['GET'])
def weather_conditions():
    """
    This is the method to show metrics of weather temperature, road temperature, wind speed of
    the road for a given period iand id or ids.

    :return: list of dictionaries or dictionary
    """
    if request.method == 'GET':

        try:
            validate_input(request.url)
        except ValidationError as e:
            return Response(
                json.dumps({"error": f"Your request URL has invalid parameters - {e}"}),
                status=400,
            )

        if request.args.get('period_end'):
            decoded_values = decode_periods_and_ids(request.args.get('ids'), request.args.get('period_start'),
                                                    request.args.get('period_end'), )
            query = db.session.query(Weather.oro_temperatura, Weather.krituliu_kiekis, Weather.rasos_taskas,
                                     Weather.vejo_greitis_vidut, Weather.vejo_greitis_maks,
                                     Weather.konstrukcijos_temp_007, Weather.konstrukcijos_temp_020,
                                     Weather.konstrukcijos_temp_050, Weather.konstrukcijos_temp_080,
                                     Weather.konstrukcijos_temp_110, Weather.konstrukcijos_temp_130,
                                     Weather.konstrukcijos_temp_140, Weather.konstrukcijos_temp_170,
                                     Weather.konstrukcijos_temp_200,
                                     Weather.sukibimo_koeficientas, Weather.dangos_temperatura, Weather.id) \
                .filter(Weather.id.in_(decoded_values[0])) \
                .filter(Weather.surinkimo_data >= decoded_values[1]) \
                .filter(Weather.surinkimo_data <= decoded_values[2]).all()
        else:
            decoded_values = decode_periods_and_ids(request.args.get('ids'), request.args.get('period_start'),
                                                    request.args.get('period_end'), )
            query = db.session.query(Weather.oro_temperatura, Weather.krituliu_kiekis, Weather.rasos_taskas,
                                     Weather.vejo_greitis_vidut, Weather.vejo_greitis_maks,
                                     Weather.konstrukcijos_temp_007, Weather.konstrukcijos_temp_020,
                                     Weather.konstrukcijos_temp_050, Weather.konstrukcijos_temp_080,
                                     Weather.konstrukcijos_temp_110, Weather.konstrukcijos_temp_130,
                                     Weather.konstrukcijos_temp_140, Weather.konstrukcijos_temp_170,
                                     Weather.konstrukcijos_temp_200,
                                     Weather.sukibimo_koeficientas, Weather.dangos_temperatura, Weather.id) \
                .filter(Weather.id.in_(decoded_values[0])) \
                .filter(Weather.surinkimo_data >= decoded_values[1]).all()

        weather_conditions_gotten_data = extract_weather_data(query, decoded_values[1], decoded_values[2])
        return weather_conditions_gotten_data


@app.route('/traffic_intensity', methods=['GET'])
def traffic_intensity():
    """
    This is the method to show average metrics of speed limits, number of Vehicles, average speed of vehicles
    in the road for a given period of an id or ids.

    :return: list of dictionaries or dictionary
    """
    if request.method == 'GET':

        try:
            validate_input(request.url)
        except ValidationError as e:
            return Response(
                json.dumps({"error": f"Your request URL has invalid parameters - {e}"}),
                status=400,
            )

        if request.args.get('period_end'):
            decoded_values = decode_periods_and_ids(request.args.get('ids'), request.args.get('period_start'),
                                                    request.args.get('period_end'), )
            query = db.session.query(Traffic.winterSpeed, Traffic.summerSpeed, Traffic.numberOfVehicles,
                                     Traffic.averageSpeed, Traffic.id, Traffic.date) \
                .filter(Traffic.id.in_(decoded_values[0])) \
                .filter(Traffic.date >= decoded_values[1]) \
                .filter(Traffic.date <= decoded_values[2]).all()
        else:
            decoded_values = decode_periods_and_ids(request.args.get('ids'), request.args.get('period_start'),
                                                    request.args.get('period_end'), )
            query = db.session.query(Traffic.winterSpeed, Traffic.summerSpeed, Traffic.numberOfVehicles,
                                     Traffic.averageSpeed, Traffic.id, Traffic.date) \
                .filter(Traffic.id.in_(decoded_values[0])) \
                .filter(Traffic.date >= decoded_values[1]).all()
        traffic_intensity_gotten_data = extract_traffic_data(query, decoded_values[1], decoded_values[2])
        return traffic_intensity_gotten_data
