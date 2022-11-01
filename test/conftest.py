import pytest
from dotenv import load_dotenv

load_dotenv(".env.testing")

import app
from app.models import Weather, Traffic


def add_data_fixtures():
    fixture_weather = Weather(
        id=363,
        surinkimo_data='2022-10-31 16:56:00.000000',
        dangos_temperatura = 7.6,
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
        pavadinimas_perspejimas='Drėgna',
        kodas='A1',
    )
    fixture_traffic = Traffic(
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
        date='2022-10-31 16:56:00.000000',
        direction='negative',
        startX=558328.3,
        startY=6068565.02,
        endX=568328.3,
        endY=6078565.02,
        winterSpeed=70,
        summerSpeed=90,
        trafficType='normal',
    )
    app.db.session.add(fixture_weather)
    app.db.session.add(fixture_traffic)
    app.db.session.commit()


@pytest.fixture(scope="module", autouse=True)
def test_client():
    with app.app.app_context():
        app.db.create_all()
        add_data_fixtures()
        testing_client = app.app.test_client()
        ctx = app.app.app_context()
        ctx.push()

        yield testing_client

    # with app.app.app_context():
        app.db.session.remove()
        app.db.drop_all()

        ctx.pop()
