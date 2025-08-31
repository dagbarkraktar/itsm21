from flask import request
from flask import jsonify
from flask_restful import Resource

from modules.maintenance.services import MaintenanceService


class MaintenanceRecordsList(Resource):
    def get(self, doc_id):
        records = MaintenanceService.get_maintenance_records(doc_id)
        return [record.to_python() for record in records]


class MaintenanceSingleRest(Resource):
    def post(self, unit_id):
        """
        Record the maintenance performed
        """
        payload = request.json
        record = MaintenanceService.save_maintenance(
            hw_id=payload['hw_id'],
            # quarter=payload['quarter'],
            # year=payload['year'],
            # performed_by_id=payload['performed_by_id'],
            notes=payload.get('notes')
        )
        return jsonify({'success': True, 'id': record.id}), 201
