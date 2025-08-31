import json

from flask import request
from flask_restful import Resource

from config import CURRENT_MAINTENANCE
from modules.hwdb.services import HwUnitsService
from modules.maintenance.services import MaintenanceService


class HwUnitsList(Resource):
    def get(self):
        filters = json.loads(request.args.get("filters", "[]"))
        hw_units = HwUnitsService.get_hw_units_list(filters)
        return hw_units


class HwUnitSingle(Resource):
    def get(self, unit_id):
        hw_unit = HwUnitsService.get_hw_unit_dict(unit_id)
        return hw_unit


class HwUnitActionMaintenance(Resource):
    def post(self, unit_id):

        doc_id = CURRENT_MAINTENANCE

        maintenance = MaintenanceService.save_maintenance(
            hw_id=unit_id,
            doc_id=doc_id
        )
        return dict(id=doc_id, m_id=maintenance.id)

    def delete(self, unit_id):

        doc_id = CURRENT_MAINTENANCE

        return MaintenanceService.delete_maintenance(
            hw_id=unit_id,
            doc_id=doc_id
        )


class HwUnitsFormularList(Resource):
    HW_SB_TYPE = 3
    HW_MON_TYPE = 27
    HW_UPS_TYPE = 28

    HW_PRINT_TYPE = 4
    HW_MFU_TYPE = 8
    HW_KMA_TYPE = 6

    WRITE_OFF_STATUSES = [7, 8, 9]

    def get(self):
        arm_units = []
        print_units = []
        mfu_units = []
        kma_units = []

        filters_actual = [
            {"field": "status_id", "op": "not_in", "val": self.WRITE_OFF_STATUSES}
        ]

        # ARM UNITS
        arm_sb_units = HwUnitsService.get_hw_list_by_type(
            type_id=self.HW_SB_TYPE,
            filters=filters_actual
        )
        for sb in arm_sb_units:
            arm_unit = []
            sb_dict = dict(
                invnum=sb.invnum,
                hw_type='Сист.блок',
                manuf=sb.manuf,
                model=sb.model,
                serialnum=sb.serialnum,
                warranty=(36 if sb.buh_os == 3 else 12),
            )
            arm_unit.append(sb_dict)

            arm_mon = HwUnitsService.get_by_invnum_n_type(
                invnum=sb.invnum, type_id=self.HW_MON_TYPE)
            if arm_mon:
                mon_dict = dict(
                    invnum=arm_mon.invnum,
                    hw_type='Монитор',
                    manuf=arm_mon.manuf,
                    model=arm_mon.model,
                    serialnum=arm_mon.serialnum,
                    warranty=(36 if arm_mon.buh_os == 3 else 12),
                )
                arm_unit.append(mon_dict)

            arm_ups = HwUnitsService.get_by_invnum_n_type(
                invnum=sb.invnum, type_id=self.HW_UPS_TYPE)
            if arm_ups:
                ups_dict = dict(
                    invnum=arm_ups.invnum,
                    hw_type='ИБП',
                    manuf=arm_ups.manuf,
                    model=arm_ups.model,
                    serialnum=arm_ups.serialnum,
                    warranty=(36 if arm_ups.buh_os == 3 else 12),
                )
                arm_unit.append(ups_dict)
            arm_units.append(arm_unit)

        # PRINT UNITS
        print_units_q = HwUnitsService.get_hw_list_by_type(
            type_id=self.HW_PRINT_TYPE,
            filters=filters_actual
        )
        for unit in print_units_q:
            print_dict = dict(
                invnum=unit.invnum,
                hw_type='Принтер',
                manuf=unit.manuf,
                model=unit.model,
                serialnum=unit.serialnum,
                warranty=(36 if unit.buh_os == 3 else 12),
            )
            print_units.append(print_dict)

        # MFU UNITS
        mfu_units_q = HwUnitsService.get_hw_list_by_type(
            type_id=self.HW_MFU_TYPE,
            filters=filters_actual
        )
        for unit in mfu_units_q:
            mfu_dict = dict(
                invnum=unit.invnum,
                hw_type='МФУ',
                manuf=unit.manuf,
                model=unit.model,
                serialnum=unit.serialnum,
                warranty=(36 if unit.buh_os == 3 else 12),
            )
            mfu_units.append(mfu_dict)

        # KMA UNITS
        kma_units_q = HwUnitsService.get_hw_list_by_type(
            type_id=self.HW_KMA_TYPE,
            filters=filters_actual
        )
        for unit in kma_units_q:
            kma_dict = dict(
                invnum=unit.invnum,
                hw_type='КМА',
                manuf=unit.manuf,
                model=unit.model,
                serialnum=unit.serialnum,
                warranty=(36 if unit.buh_os == 3 else 12),
            )
            kma_units.append(kma_dict)

        return dict(
            arm_units=arm_units,
            print_units=print_units,
            mfu_units=mfu_units,
            kma_units=kma_units,
        )
