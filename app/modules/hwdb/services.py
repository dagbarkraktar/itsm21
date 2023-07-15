from modules.hwdb.models import HwDbModel
from models.mixins import FilterMixin


class HwUnitsService(FilterMixin):

    @classmethod
    def get_hw_units_list(cls, filters=None):
        query = HwDbModel.query
        query = query.order_by(HwDbModel.id.desc())
        query = cls.apply_filters(query, HwDbModel, filters)
        # query = query.limit(limit).offset(offset)
        hw_units = query.all()

        hw_units_list = [
            unit.to_python()
            for unit in hw_units
        ]

        return hw_units_list

    @classmethod
    def get_hw_unit_dict(cls, unit_id):
        hw_unit = HwDbModel.query.get(unit_id)
        if not hw_unit:
            return None
        hw_unit_dict = hw_unit.to_python()

        return hw_unit_dict
