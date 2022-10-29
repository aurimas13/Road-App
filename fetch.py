from datetime import datetime

import requests
from app import app, db
from sqlalchemy import func
from app.models import Weather, Traffic, BatchUpdate
from src.data_validation import WeatherValidate, TrafficValidate
from pprint import PrettyPrinter

pp = PrettyPrinter()

# Fetch Data
url_weather = 'https://eismoinfo.lt/weather-conditions-service'
url_traffic = 'https://eismoinfo.lt/traffic-intensity-service'
response = requests.get(url_weather)
resp = response.json()
response_traffic = requests.get(url_traffic)
resp_traffic = response_traffic.json()
# CURRENT_DATE = datetime.now().strftime('%Y-%m-%d %H:%M')

with app.app_context():
    # date = datetime.strptime("2022-10-01 14:00:00", '%Y-%m-%d %X')
    result = db.session.query(BatchUpdate).order_by(BatchUpdate.batchUpdateDate.desc()).first() # Tik ideda pasikartojancias datas, kaip to isvengti?
    batch_date = datetime.strptime(str(result), '%Y-%m-%d %X') if result is not None else datetime.strptime("1970-01-01 00:00:00", '%Y-%m-%d %X')
    # idx = db.session.query(BatchUpdate).filter(BatchUpdate.batchId == BatchUpdate.batchId, func.max(BatchUpdate.batchUpdateDate)).first()
    # pp.pprint(idx)
    pp.pprint(result)
    pp.pprint(type(result))
    pp.pprint(datetime.strftime(batch_date, '%Y-%m-%d %H:%M'))
    pp.pprint(type(batch_date))

    new_batch_update = BatchUpdate(
        batchUpdateDate=batch_date
    )
    db.session.add(new_batch_update)
    db.session.commit()

    pp.pprint(new_batch_update.batchId)

    if resp[0]["surinkimo_data"] > datetime.strftime(batch_date, '%Y-%m-%d %H:%M'):
        batch_date = resp[0]["surinkimo_data"]
        new_batch_update = BatchUpdate(
            batchUpdateDate=datetime.strptime(batch_date, '%Y-%m-%d %H:%M'),
        )
        db.session.add(new_batch_update)
        db.session.commit()

        pp.pprint(resp[0]["surinkimo_data"])
        pp.pprint(new_batch_update.batchId)
        for json_value in resp[:10]:
                WeatherValidate().load(json_value)
                pavadinimas_perspejimas = None
                kodas = None
                if "perspejimai" in json_value:
                    for i in range(len(json_value['perspejimai'])):
                        pavadinimas_perspejimas = json_value["perspejimai"][i]['pavadinimas']
                        kodas = json_value["perspejimai"][i]['kodas']

                weather_properties = Weather(
                    surinkimo_data_unix=json_value["surinkimo_data_unix"],  # reikia kad butu unix date
                    surinkimo_data=datetime.strptime(json_value["surinkimo_data"], '%Y-%m-%d %H:%M'),
                    weather_auto_id=json_value["id"],
                    irenginys=json_value["irenginys"],
                    numeris=json_value["numeris"],
                    pavadinimas=json_value["pavadinimas"],
                    kilometras=json_value["kilometras"],
                    oro_temperatura=json_value["oro_temperatura"],
                    vejo_greitis_vidut=json_value["vejo_greitis_vidut"],
                    krituliu_tipas=json_value["krituliu_tipas"],
                    krituliu_kiekis=json_value["krituliu_kiekis"],
                    dangos_temperatura=json_value["dangos_temperatura"],
                    matomumas=json_value["matomumas"],
                    rasos_taskas=json_value["rasos_taskas"],
                    kelio_danga=json_value["kelio_danga"],
                    uzsalimo_taskas=json_value["uzsalimo_taskas"],
                    vejo_greitis_maks=json_value["vejo_greitis_maks"],
                    vejo_kryptis=json_value["vejo_kryptis"],
                    sukibimo_koeficientas=json_value["sukibimo_koeficientas"],
                    ilguma=json_value["ilguma"],
                    platuma=json_value["platuma"],
                    lat=json_value["lat"],
                    lng=json_value["lng"],
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


        for json_value in resp_traffic[:10]:
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
                    direction=road_segment['direction'],
                    startX=road_segment["startX"],
                    startY=road_segment["startY"],
                    endX=road_segment["endX"],
                    endY=road_segment["endY"],
                    winterSpeed=road_segment["winterSpeed"],
                    summerSpeed=road_segment["summerSpeed"],
                    numberOfVehicles=road_segment["numberOfVehicles"],
                    averageSpeed=road_segment["averageSpeed"],
                    trafficType=road_segment["trafficType"],
                    batchId=new_batch_update.batchId
                )
                db.session.add(traffic_intensity)
                db.session.commit()
