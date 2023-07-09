import json

from flask import request
from flask_restful import Resource

from modules.hwdb.services import HwUnitsService


class HwUnitsList(Resource):
    def get(self):
        filters = json.loads(request.args.get("filters", "[]"))
        hw_units = HwUnitsService.get_hw_units_list(filters)
        return hw_units


class HwUnitSingle(Resource):
    def get(self, unit_id):
        hw_unit = HwUnitsService.get_hw_unit_dict(unit_id)
        return hw_unit
