from app_setup import db


class SensorsLog(db.Model):
    __tablename__ = 'sensors_log'

    id = db.Column(db.BigInteger, primary_key=True)
    timestamp_utc = db.Column(db.DateTime)
    sensor_id = db.Column(db.Integer)
    sensor_tag = db.Column(db.String(32))
    sensor_value_string = db.Column(db.String(128))
    sensor_value_float = db.Column(db.Float)
