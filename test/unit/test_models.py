import glob
import unittest
import sys
import os
from datetime import datetime

import pytz

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)
from app.models import Weather, Traffic


def test_new_weather_schema():
    """
    GIVEN a Weather model
    WHEN a new Weather is created
    THEN check Weather schema attributes
    """
    weather = Weather(
        id=363,
        surinkimo_data=datetime.strptime('2022-10-30 16:56:00.000000', '%Y-%m-%d %X.%f').replace(tzinfo=pytz.UTC),
        dangos_temperatura=7.6,
        oro_temperatura=5.9,
        krituliu_kiekis=0.5,
        rasos_taskas=2.7,
        sukibimo_koeficientas=0.8,
        vejo_greitis_vidut=1.0,
        vejo_greitis_maks=1.4,
        konstrukcijos_temp_007=9.6,
        konstrukcijos_temp_020=10,
        konstrukcijos_temp_050=10.8,
        konstrukcijos_temp_080=11.7,
        konstrukcijos_temp_110=12.6,
        konstrukcijos_temp_130=7.0,
        konstrukcijos_temp_140=12.9,
        konstrukcijos_temp_170=12.6,
        konstrukcijos_temp_200=12.9,
        pavadinimas='Drėgna',
        kodas='A1',
    )
    assert weather.id == 362
    assert weather.surinkimo_data == datetime.strptime('2022-10-30 16:56:00.000000', '%Y-%m-%d %X.%f').replace(tzinfo=pytz.UTC)
    assert weather.dangos_temperatura == 7.6
    assert weather.oro_temperatura == 5.9
    assert weather.krituliu_kiekis == 0.5
    assert weather.rasos_taskas == 2.7
    assert weather.sukibimo_koeficientas == 0.8
    assert weather.vejo_greitis_vidut == 1.0
    assert weather.vejo_greitis_maks == 1.4
    assert weather.konstrukcijos_temp_007 == 9.6
    assert weather.konstrukcijos_temp_020 == 10
    assert weather.konstrukcijos_temp_050 == 10.8
    assert weather.konstrukcijos_temp_080 == 11.7
    assert weather.konstrukcijos_temp_110 == 12.6
    assert weather.konstrukcijos_temp_130 == 7.0
    assert weather.konstrukcijos_temp_140 == 12.9
    assert weather.konstrukcijos_temp_170 == 12.6
    assert weather.konstrukcijos_temp_200 == 12.9
    assert weather.pavadinimas == 'Drėgna'
    assert weather.kodas == 'A1'


def test_new_traffic_schema():
    """
    GIVEN a Traffic model
    WHEN a new Traffic is created
    THEN check Traffic schema attributes
    """
    traffic = Traffic(
        id=3611,
        averageSpeed=84.1,
        numberOfVehicles=70,
        traffic_name='G1',
        road_number='A1',
        road_name='Vilnius-Kaunas-Klaipėda',
        km=117.1,
        x=55.8328,
        y=60.7856,
        timeInterval=15,
        date=datetime.strptime('2022-10-31 16:56:00.000000', '%Y-%m-%d %X.%f').replace(tzinfo=pytz.UTC),
        direction='negative',
        startX=558328.3,
        startY=6068565.02,
        endX=568328.3,
        endY=6078565.02,
        winterSpeed=70,
        summerSpeed=90,
        trafficType='normal',
    )
    assert traffic.id == 3611
    assert traffic.averageSpeed == 84.1
    assert traffic.numberOfVehicles == 70
    assert traffic.traffic_name == 'G1'
    assert traffic.road_number == 'A1'
    assert traffic.road_name == 'Vilnius-Kaunas-Klaipėda'
    assert traffic.km == 117.1
    assert traffic.x == 55.8328
    assert traffic.y == 60.7856
    assert traffic.timeInterval == 15
    assert traffic.date == datetime.strptime('2022-10-31 16:56:00.000000', '%Y-%m-%d %X.%f').replace(tzinfo=pytz.UTC)
    assert traffic.direction == 'negative'
    assert traffic.startX == 558328.3
    assert traffic.startY == 6068565.02
    assert traffic.endX == 568328.3
    assert traffic.endY == 6078565.02
    assert traffic.winterSpeed == 70
    assert traffic.summerSpeed == 90
    assert traffic.trafficType == 'normal'


if __name__ == '__main__':
    unittest.main()