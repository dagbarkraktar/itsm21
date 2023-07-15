"""
Import data to DB from JSON file
"""
import json
from datetime import datetime

from app_setup import db, create_app
from modules.hwdb.models import HwDbModel, HwTypesModel, HwStatusesModel
from models.employees import EmplListGasModel
from models.maintenance import MaintenanceDocsDbModel, MaintenanceDbModel

HWDB_JSON_DUMP = '../dumps/hwdb_2023-05-18.json'
HWTYPES_JSON_DUMP = '../dumps/hw_types_2023-05-18.json'
HWSTASUS_JSON_DUMP = '../dumps/hw_statuses_2023-05-18.json'
EMPL_JSON_DUMP = '../dumps/empl_list_gas_2023-05-18.json'
MNT_JSON_DUMP = '../dumps/mnt_2023-05-18.json'
MNT_DOCS_JSON_DUMP = '../dumps/mnt_docs_2023-05-18.json'


if __name__ == "__main__":
    app = create_app()
    with app.app_context():

        # HwTypesModel
        print('Import HwTypesModel from JSON')
        with open(HWTYPES_JSON_DUMP, 'r') as fp:
            data = json.load(fp) or []
            for line in data:
                unit = HwTypesModel(
                    id=line.get('id'),
                    hw_type=line.get('hw_type'),
                    hw_type_ru=line.get('hw_type_ru')
                )
                db.session.add(unit)
                db.session.commit()

        # HwStatusesModel
        print('Import HwStatusesModel from JSON')
        with open(HWSTASUS_JSON_DUMP, 'r') as fp:
            data = json.load(fp) or []
            for line in data:
                unit = HwStatusesModel(
                    id=line.get('id'),
                    status_name=line.get('status_name'),
                    status_name_ru=line.get('status_name_ru')
                )
                db.session.add(unit)
                db.session.commit()

        # EmplListGasModel
        print('Import EmplListGasModel from JSON')
        with open(EMPL_JSON_DUMP, 'r') as fp:
            data = json.load(fp) or []
            for line in data:
                # due to date mess in input data
                # date_recr
                date_recr_str = line.get('date_recr', None)
                if not date_recr_str or date_recr_str == '0':
                    date_recr_str = '01.01.1970'
                date_recr = datetime.strptime(date_recr_str, '%d.%m.%Y').date()
                # date_post
                date_post_str = line.get('date_post', None)
                if not date_post_str or date_post_str == '0':
                    date_post_str = '01.01.1970'
                date_post = datetime.strptime(date_post_str, '%d.%m.%Y').date()
                # date_birth
                date_birth_str = line.get('date_birth', None)
                if not date_birth_str or date_birth_str == '0':
                    date_birth_str = '01.01.1970'
                date_birth = datetime.strptime(date_birth_str, '%d.%m.%Y').date()

                unit = EmplListGasModel(
                    id=line.get('id'),
                    fio=line.get('fio'),
                    tab_no=line.get('tab_no'),
                    depts=line.get('depts'),
                    post=line.get('post'),
                    post_dop=line.get('post_dop'),
                    date_recr=date_recr,
                    date_post=date_post,
                    sx=line.get('sx'),
                    date_birth=date_birth
                )
                db.session.add(unit)
                db.session.commit()

        # MaintenanceDocsDbModel
        print('Import MaintenanceDocsDbModel from JSON')
        with open(MNT_DOCS_JSON_DUMP, 'r') as fp:
            data = json.load(fp) or []
            for line in data:
                unit = MaintenanceDocsDbModel(
                    id=line.get('id'),
                    year=line.get('year'),
                    num_thru_year=line.get('num_thru_year'),
                    doc_date=line.get('doc_date'),
                    doc_num=line.get('doc_num'),
                    units_qty=line.get('units_qty'),
                    units_id_list=line.get('units_id_list')
                )
                db.session.add(unit)
                db.session.commit()

        # MaintenanceDbModel
        print('Import MaintenanceDbModel from JSON')
        with open(MNT_JSON_DUMP, 'r') as fp:
            data = json.load(fp) or []
            for line in data:
                unit = MaintenanceDbModel(
                    id=line.get('id'),
                    doc_id=line.get('doc_id'),
                    hw_unit_id=line.get('hw_unit_id'),
                    status_id=line.get('status_id')
                )
                db.session.add(unit)
                db.session.commit()

        # HWDB
        print('Import HWDB from JSON')
        with open(HWDB_JSON_DUMP, 'r') as fp:
            data = json.load(fp) or []
            for line in data:
                unit = HwDbModel()
                unit.id = line.get('id')
                unit.invnum = line.get('invnum')
                print(unit.invnum)
                unit.type_id = line.get('type_id')
                unit.legacy_user = line.get('legacy_user')
                unit.empl_id = line.get('empl_id')
                unit.location = line.get('location')
                unit.status_id = line.get('status_id')
                unit.manuf = line.get('manuf')
                unit.model = line.get('model')
                unit.vendor_id = line.get('vendor_id')
                unit.serialnum = line.get('serialnum')
                unit.year = line.get('year')
                unit.warranty = line.get('warranty')
                unit.accounting = line.get('accounting')
                unit.comments = line.get('comments')
                unit.buhtext = line.get('buhtext')
                unit.buh_os = line.get('buh_os')
                unit.check = line.get('check')
                unit.last_maintenance_id = line.get('last_maintenance_id')
                db.session.add(unit)
                db.session.commit()
