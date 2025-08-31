from sqlalchemy import asc

from app_setup import db
from modules.hwdb.models import HwDbModel
from modules.maintenance.models import MaintenanceRecordModel


class MaintenanceService:
    @staticmethod
    def get_hardware_due_for_maintenance(quarter, year):
        """
        Get a list of equipment that requires maintenance in the specified period
        """
        subquery = db.session.query(MaintenanceRecordModel.hw_id) \
            .filter(MaintenanceRecordModel.quarter == quarter,
                    MaintenanceRecordModel.year == year)

        return HwDbModel.query.filter(~HwDbModel.id.in_(subquery)).all()

    @staticmethod
    def save_maintenance(hw_id, doc_id, notes=None):
        """
        Save maintenance record
        """
        db_record = MaintenanceRecordModel.query.filter(
            MaintenanceRecordModel.hw_id == hw_id,
            MaintenanceRecordModel.doc_id == doc_id
        ).first()
        if db_record:
            print('Maintenance Record for unit #{} already exist!'.format(hw_id))
            return db_record

        record = MaintenanceRecordModel(
            hw_id=hw_id,
            doc_id=doc_id,
            notes=notes
        )
        db.session.add(record)
        db.session.commit()
        return record

    @staticmethod
    def delete_maintenance(hw_id, doc_id):
        """
        Delete maintenance record
        """
        db_record = MaintenanceRecordModel.query.filter(
            MaintenanceRecordModel.hw_id == hw_id,
            MaintenanceRecordModel.doc_id == doc_id
        ).first()
        if not db_record:
            print('Maintenance Record for unit #{} not found!'.format(hw_id))
            return dict(result='not found')

        result = dict(
            m_id=db_record.id,
            doc_id=db_record.doc_id,
            hw_id=db_record.hw_id,
        )

        db.session.delete(db_record)
        db.session.commit()
        return result

    @staticmethod
    def get_maintenance_records(doc_id):
        query = MaintenanceRecordModel.query
        query = query.filter(MaintenanceRecordModel.doc_id == doc_id).join(MaintenanceRecordModel.hardware)
        query = query.order_by(
            asc(HwDbModel.invnum),
            asc(HwDbModel.type_id),
        )
        return query.all()

    @staticmethod
    def get_maintenance_report(quarter=None, year=None):
        """
        Get a report on the maintenance performed with filtering
        """
        query = MaintenanceRecordModel.query

        if quarter:
            query = query.filter(MaintenanceRecordModel.quarter == quarter)
        if year:
            query = query.filter(MaintenanceRecordModel.year == year)

        return query.order_by(MaintenanceRecordModel.maintenance_date.desc()).all()
