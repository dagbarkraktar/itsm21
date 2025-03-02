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

    @classmethod
    def get_by_invnum_n_serial(cls, invnum, serialnum):
        if not invnum and not serialnum:
            return None
        query = HwDbModel.query
        if invnum:
            query = query.filter(HwDbModel.invnum == invnum)
        if serialnum:
            query = query.filter(HwDbModel.serialnum == serialnum)
        return query.first()

    @classmethod
    def get_by_invnum_n_type(cls, invnum, type_id):
        if not invnum:
            return None
        query = HwDbModel.query
        query = query.filter(HwDbModel.invnum == invnum)
        if type_id:
            query = query.filter(HwDbModel.type_id == type_id)
        return query.first()

    @classmethod
    def get_hw_tomsk_models_list(cls, filters=None):
        query = HwTomskModels.query
        query = query.order_by(HwTomskModels.id.asc())
        query = cls.apply_filters(query, HwTomskModels, filters)
        units = query.all()

        return units
