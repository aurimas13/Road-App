import json
from urllib import parse

from flask import Response
from marshmallow import ValidationError, validate, Schema, fields


def validate_input(url):
    request_dict = dict(
        parse.parse_qsl(
            parse.urlsplit(parse.unquote(url)).query
        )
    )
    return RequestValidate().load(request_dict)


class Perspejimai(Schema):
    pavadinimas = fields.Str(required=False, allow_none=True)
    kodas = fields.Str(required=False, allow_none=True)


class WeatherValidate(Schema):
    id = fields.Integer(required=True)
    surinkimo_data = fields.Str(required=True, allow_none=True)
    oro_temperatura = fields.Float(required=True, allow_none=True)
    vejo_greitis_vidut = fields.Float(required=True, allow_none=True)
    krituliu_kiekis = fields.Float(required=True, allow_none=True)
    dangos_temperatura = fields.Float(required=True, allow_none=True)
    rasos_taskas = fields.Float(required=True, allow_none=True)
    vejo_greitis_maks = fields.Float(required=True, allow_none=True)
    sukibimo_koeficientas = fields.Float(required=True, allow_none=True)
    konstrukcijos_temp_007 = fields.Float(required=True, allow_none=True)
    konstrukcijos_temp_020 = fields.Float(required=True, allow_none=True)
    konstrukcijos_temp_050 = fields.Float(required=True, allow_none=True)
    konstrukcijos_temp_080 = fields.Float(required=True, allow_none=True)
    konstrukcijos_temp_110 = fields.Float(required=True, allow_none=True)
    konstrukcijos_temp_130 = fields.Float(required=True, allow_none=True)
    konstrukcijos_temp_140 = fields.Float(required=True, allow_none=True)
    konstrukcijos_temp_170 = fields.Float(required=True, allow_none=True)
    konstrukcijos_temp_200 = fields.Float(required=True, allow_none=True)
    kelio_danga = fields.Str(required=False, allow_none=True)
    uzsalimo_taskas = fields.Str(required=False, allow_none=True)
    vejo_kryptis = fields.Str(required=False, allow_none=True)
    irenginys = fields.Str(required=False, allow_none=True)
    numeris = fields.Str(required=False, allow_none=True)
    pavadinimas = fields.Str(required=False, allow_none=True)
    krituliu_tipas = fields.Str(required=False, allow_none=True)
    surinkimo_data_unix = fields.Integer(required=False, allow_none=True)
    matomumas = fields.Integer(required=False, allow_none=True)
    kilometras = fields.Float(required=False, allow_none=True)
    ilguma = fields.Float(required=False)
    platuma = fields.Float(required=False)
    lat = fields.Float(required=False)
    lng = fields.Float(required=False)
    perspejimai = fields.List(fields.Nested(Perspejimai))


class RoadSegments(Schema):
    direction = fields.Str(required=True, allow_none=True)
    startX = fields.Float(required=True, allow_none=True)
    startY = fields.Float(required=True, allow_none=True)
    endX = fields.Float(required=True, allow_none=True)
    endY = fields.Float(required=True, allow_none=True)
    winterSpeed = fields.Integer(required=True)
    summerSpeed = fields.Integer(required=True)
    numberOfVehicles = fields.Integer(required=True)
    averageSpeed = fields.Float(required=True, allow_none=True)
    trafficType = fields.Str(required=True, allow_none=True)


class TrafficValidate(Schema):
    id = fields.Integer(required=True)
    name = fields.Str(required=True, allow_none=True)
    roadNr = fields.Str(required=True, allow_none=True)
    roadName = fields.Str(required=True, allow_none=True)
    km = fields.Float(required=True, allow_none=True)
    x = fields.Float(required=True, allow_none=True)
    y = fields.Float(required=True, allow_none=True)
    timeInterval = fields.Integer(required=True, allow_none=True)
    date = fields.Str(required=True, allow_none=True)
    roadSegments = fields.List(fields.Nested(RoadSegments))


class BatchValidate(Schema):
    baltchId = fields.Integer(required=True, allow_none=False)
    batchUpdateDate = fields.Str(required=True, allow_none=True)


class RequestValidate(Schema):
    ids = fields.Str(required=True, allow_none=False, validate=[validate.Regexp(r"^[0-9]+(?:,[0-9]+)*$"),
                                                                validate.Length(min=1)])
    period_start = fields.DateTime(required=True, allow_none=False, format='%Y-%m-%d %X')
    period_end = fields.DateTime(required=False, allow_none=True, format='%Y-%m-%d %X')
