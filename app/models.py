from app import db


class Weather(db.Model):

    """    Weather Conditions Schema    """
    weather_auto_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, nullable=True)
    surinkimo_data_unix = db.Column(db.Integer, nullable=True)
    matomumas = db.Column(db.Integer, nullable=True)
    kilometras = db.Column(db.REAL, nullable=True)
    oro_temperatura = db.Column(db.REAL, nullable=True)
    vejo_greitis_vidut = db.Column(db.REAL, nullable=True)
    krituliu_kiekis = db.Column(db.REAL, nullable=True)
    dangos_temperatura = db.Column(db.REAL, nullable=True)
    rasos_taskas = db.Column(db.REAL, nullable=True)
    vejo_greitis_maks = db.Column(db.REAL, nullable=True)
    sukibimo_koeficientas = db.Column(db.REAL, nullable=True)
    ilguma = db.Column(db.REAL, nullable=True)
    platuma = db.Column(db.REAL, nullable=True)
    lat = db.Column(db.REAL, nullable=True)
    lng = db.Column(db.REAL, nullable=True)
    konstrukcijos_temp_007 = db.Column(db.REAL, nullable=True)
    konstrukcijos_temp_020 = db.Column(db.REAL, nullable=True)
    konstrukcijos_temp_050 = db.Column(db.REAL, nullable=True)
    konstrukcijos_temp_080 = db.Column(db.REAL, nullable=True)
    konstrukcijos_temp_110 = db.Column(db.REAL, nullable=True)
    konstrukcijos_temp_130 = db.Column(db.REAL, nullable=True)
    konstrukcijos_temp_140 = db.Column(db.REAL, nullable=True)
    konstrukcijos_temp_170 = db.Column(db.REAL, nullable=True)
    konstrukcijos_temp_200 = db.Column(db.REAL, nullable=True)
    kelio_danga = db.Column(db.String(140), nullable=True)
    uzsalimo_taskas = db.Column(db.String(64), nullable=True)
    vejo_kryptis = db.Column(db.String(64), nullable=True)
    surinkimo_data = db.Column(db.DateTime, nullable=True)
    irenginys = db.Column(db.String(140), nullable=True)
    numeris = db.Column(db.String(140), nullable=True)
    pavadinimas = db.Column(db.String(140), nullable=True)
    krituliu_tipas = db.Column(db.String(140), nullable=True)
    pavadinimas_perspejimas = db.Column(db.String(140), nullable=True)
    kodas = db.Column(db.String(140), nullable=True)
    batchId = db.Column(db.Integer, db.ForeignKey('batch_update.batchId'), nullable=True)

    def __repr__(self):
        return '<Weather Condition of {} with id {}>'.format(self.pavadinimas, self.id)


class Traffic(db.Model):

    """     Traffic Intensity Schema     """
    traffic_auto_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, nullable=True)
    traffic_name = db.Column(db.String(140), nullable=True)
    road_number = db.Column(db.String(64), nullable=True)
    road_name = db.Column(db.String(140), nullable=True)
    km = db.Column(db.REAL, nullable=True)
    x = db.Column(db.REAL, nullable=True)
    y = db.Column(db.REAL, nullable=True)
    timeInterval = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    direction = db.Column(db.String(64), nullable=True)
    startX = db.Column(db.REAL, nullable=True)
    startY = db.Column(db.REAL, nullable=True)
    endX = db.Column(db.REAL, nullable=True)
    endY = db.Column(db.REAL, nullable=True)
    winterSpeed = db.Column(db.Integer, nullable=True)
    summerSpeed = db.Column(db.Integer, nullable=True)
    numberOfVehicles = db.Column(db.Integer, nullable=True)
    averageSpeed = db.Column(db.REAL, nullable=True)
    trafficType = db.Column(db.String(140), nullable=True)
    batchId = db.Column(db.Integer, db.ForeignKey('batch_update.batchId'), nullable=True)

    def __repr__(self):
        return '<Traffic {} of id {} has average speed of {}>'.format(self.traffic_name, self.id, self.averageSpeed)


class BatchUpdate(db.Model):

    """     BatchUpdate Schema     """
    batchId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    batchUpdateDate = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '{}'.format(self.batchUpdateDate)
