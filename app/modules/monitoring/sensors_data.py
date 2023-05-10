import datetime
import logging

from flask import jsonify
from flask_restful import Resource

from modules.monitoring.models import SensorsLog
import log.log_config

MAX_SENSOR_NUM = 2
UTC_TO_MSK_OFFSET = 3

sensor_logger = logging.getLogger('sensor_log')


class Sensors(Resource):

    def get(self, sensor_id):
        sensor_data = []
        sid = sensor_id if sensor_id < MAX_SENSOR_NUM else 1

        sensor_logger.debug(f'SensorID={sid}')

        try:
            dt_utcnow = datetime.datetime.utcnow()
            delta = datetime.timedelta(hours=24, minutes=0, seconds=0)
            sensor_log = (SensorsLog.query
                          .filter(SensorsLog.timestamp_utc > (dt_utcnow - delta))
                          .filter(SensorsLog.sensor_id == sid)
                          .all())
            for line in sensor_log:
                sensor_data.append(
                    dict(
                        dt=line.timestamp_utc + datetime.timedelta(hours=UTC_TO_MSK_OFFSET),
                        value=line.sensor_value_string,
                    )
                )

        except Exception as e:
            print('ERROR: Requesting sensor data! {}'.format(e))
            sensor_logger.error('ERROR: Requesting sensor data! {}'.format(e))

        return jsonify(sensor_data)
