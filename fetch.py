import os
import pytz
from app import app, db
from app.models import Weather, Traffic, BatchUpdate
from app.data_validation import WeatherValidate, TrafficValidate
from app.helper import fetch_data, change_date_to_utc
from datetime import datetime

# Define variables
URL_WEATHER_DATABASE = os.getenv("URL_WEATHER_DATABASE")
URL_TRAFFIC_DATABASE = os.getenv("URL_TRAFFIC_DATABASE")
CURRENT_DATE = datetime.utcnow()

# Fetch Data
resp_weather = fetch_data(URL_WEATHER_DATABASE)
resp_traffic = fetch_data(URL_TRAFFIC_DATABASE)

with app.app_context():
    result = db.session.query(BatchUpdate).order_by(
        BatchUpdate.batchUpdateDate.desc()).first()  # Tik ideda pasikartojancias datas, kaip to isvengti?
    batch_date = datetime.strptime(str(result), '%Y-%m-%d %X.%f').replace(tzinfo=pytz.UTC) if result is not None else \
        datetime.strptime("1970-01-01 00:00:00", '%Y-%m-%d %X').replace(tzinfo=pytz.UTC)

    new_batch_update = BatchUpdate(
        batchUpdateDate=CURRENT_DATE
    )
    db.session.add(new_batch_update)
    db.session.commit()

    for json_value in resp_weather:

        utc_date = change_date_to_utc(json_value["surinkimo_data"])
        if utc_date > batch_date:
            WeatherValidate().load(json_value)
            pavadinimas_perspejimas = None
            kodas = None

            if "perspejimai" in json_value:
                for i in range(len(json_value['perspejimai'])):
                    pavadinimas_perspejimas = json_value["perspejimai"][i]['pavadinimas']
                    kodas = json_value["perspejimai"][i]['kodas']

            weather_properties = Weather(
                id=json_value["id"],
                surinkimo_data=utc_date,
                oro_temperatura=json_value["oro_temperatura"],
                vejo_greitis_vidut=json_value["vejo_greitis_vidut"],
                krituliu_kiekis=json_value["krituliu_kiekis"],
                dangos_temperatura=json_value["dangos_temperatura"],
                rasos_taskas=json_value["rasos_taskas"],
                vejo_greitis_maks=json_value["vejo_greitis_maks"],
                sukibimo_koeficientas=json_value["sukibimo_koeficientas"],
                konstrukcijos_temp_007=json_value["konstrukcijos_temp_007"],
                konstrukcijos_temp_020=json_value["konstrukcijos_temp_020"],
                konstrukcijos_temp_050=json_value["konstrukcijos_temp_050"],
                konstrukcijos_temp_080=json_value["konstrukcijos_temp_080"],
                konstrukcijos_temp_110=json_value["konstrukcijos_temp_110"],
                konstrukcijos_temp_130=json_value["konstrukcijos_temp_130"],
                konstrukcijos_temp_140=json_value["konstrukcijos_temp_140"],
                konstrukcijos_temp_170=json_value["konstrukcijos_temp_170"],
                konstrukcijos_temp_200=json_value["konstrukcijos_temp_200"],
                pavadinimas_perspejimas=pavadinimas_perspejimas,
                kodas=kodas,
                batchId=new_batch_update.batchId
            )

            db.session.add(weather_properties)
            db.session.commit()

    for json_value in resp_traffic:
        s1 = set()
        if datetime.strptime(json_value["date"], '%Y-%m-%dT%H:%M:%S.%f%z').replace(tzinfo=pytz.UTC) > batch_date:
            if json_value['roadSegments']:
                for i in range(len(json_value['roadSegments'])):
                    road_segment = json_value["roadSegments"][i]
                    TrafficValidate().load(json_value)
                    traffic_intensity = Traffic(
                        id=json_value["id"],
                        traffic_name=json_value["name"],
                        road_number=json_value["roadNr"],
                        road_name=json_value["roadName"],
                        km=json_value["km"],
                        x=json_value["x"],
                        y=json_value["y"],
                        timeInterval=json_value["timeInterval"],
                        date=datetime.strptime(json_value["date"], '%Y-%m-%dT%H:%M:%S.%f%z'),
                        batchId=new_batch_update.batchId,
                        direction=road_segment['direction'],
                        startX=road_segment["startX"],
                        startY=road_segment["startY"],
                        endX=road_segment["endX"],
                        endY=road_segment["endY"],
                        winterSpeed=road_segment["winterSpeed"],
                        summerSpeed=road_segment["summerSpeed"],
                        numberOfVehicles=road_segment["numberOfVehicles"],
                        averageSpeed=road_segment["averageSpeed"],
                        trafficType=road_segment["trafficType"]
                    )
                    db.session.add(traffic_intensity)
                    db.session.commit()
