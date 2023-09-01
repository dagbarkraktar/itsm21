from flask import jsonify
from flask_restful import Resource
import redis
import json

from config import REDIS_HOST, REDIS_PORT

MAX_RECORDS_QTY = 10


class Backups(Resource):
    """ Endpoint '/api/v1/backups' implementation """
    def get(self):

        try:
            # redis_db = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
            redis_db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

            response = {}
            sdp_backups_data = []
            oracle_backups_data = []
            buhsrv_backups_data = []
            sudimost_backups_data = []

            # Get last MAX_RECORDS_QTY values for each backups list
            raw_list = redis_db.lrange('sdp_backup_list', -MAX_RECORDS_QTY, -1)
            for item in raw_list:
                sdp_backups_data.append(json.loads(bytes.decode(item)))

            raw_list = redis_db.lrange('oracle_backup_list', -MAX_RECORDS_QTY, -1)
            for item in raw_list:
                oracle_backups_data.append(json.loads(bytes.decode(item)))

            raw_list = redis_db.lrange('buhsrv_backup_list', -MAX_RECORDS_QTY, -1)
            for item in raw_list:
                buhsrv_backups_data.append(json.loads(bytes.decode(item)))

            raw_list = redis_db.lrange('sudimost_backup_list', -MAX_RECORDS_QTY, -1)
            for item in raw_list:
                sudimost_backups_data.append(json.loads(bytes.decode(item)))

            response['sdp_backup'] = sdp_backups_data
            response['oracle_backup'] = oracle_backups_data
            response['buhsrv_backup'] = buhsrv_backups_data
            response['sudimost_backup'] = sudimost_backups_data

        except Exception as e:
            # TODO: Add logging
            print(f'Redis DB error: {e}')
            return {'message': 'Redis DB Error!'}, 500

        #  Return dict with data as json
        return jsonify(response)
