import os

import werkzeug
import sys
from app.models import Weather, Traffic, BatchUpdate
from flask import render_template, flash, redirect, url_for, request, Response
from app import app, db
from pprint import PrettyPrinter
pp = PrettyPrinter()
from fetch import *


APP_BASE_URL = os.getenv("APP_BASE_URL")
PORT = os.getenv("PORT")

@app.route('/', methods=['GET'])
@app.route('/weather_conditions', methods=['GET'])
def weather_conditions():
    """
    This is the method to show metrics of weather temperature, road temperature, wind speed, wind direction,
    visibility of the road for a given period in a road of an id or ids.

    Query models of Story, Task & TaskActualTimes in query_result and
    returns a list (stories) after they are filtered.

    return:
        render_template (str) for getting template
    """
    weathers = Weather.query.filter_by(id='mini').order_by(Weather.name).all()
    sock_text = '<ul>'
    for weather in weathers:
        sock_text += '<li>' + weather.name + ', ' + weather.id + '</li>'
    sock_text += '</ul>'
    return sock_text

    # file =
    # pp.print(file)


@app.route('/traffic_intensity', methods=['GET'])
def traffic_intensity():
    """
    This is the method to show metrics of speed limits, number of Vehicles, avergae speed of vehicles
    in the road for a given period of an id or ids.

    Query models of Task & TaskActualTimes in query_result and
    Story, Task & TaskActualTimes in query_result2 while
    returning lists (tasks & stories) after they are filtered.

    args:
        id (str) for retrieving story id

    return:
        render_template (str) for getting template
    """
    pp.pprint("HAHA")

