from app_setup import db

from models.employees import EmplListGasModel
from models.maintenance import MaintenanceDbModel, MaintenanceDocsDbModel


class HwDbModel(db.Model):
    __tablename__ = 'hw_db'

    id = db.Column(db.BigInteger, primary_key=True)
    invnum = db.Column(db.String(20))
    type_id = db.Column(db.Integer, db.ForeignKey('hw_types.id', ondelete='CASCADE'))
    hw_type = db.relationship('HwTypesModel', backref='hw_db', lazy='joined')
    legacy_user = db.Column(db.String(50))
    empl_id = db.Column(db.Integer, db.ForeignKey('empl_list_gas.id', ondelete='CASCADE'))
    empl_fio = db.relationship('EmplListGasModel', backref='hw_db', lazy='joined')
    location = db.Column(db.String(4))
    status_id = db.Column(db.Integer, db.ForeignKey('hw_statuses.id', ondelete='CASCADE'))
    status = db.relationship('HwStatusesModel', backref='hw_db', lazy='joined')
    manuf = db.Column(db.String(20))
    model = db.Column(db.String(64))
    vendor_id = db.Column(db.Integer)
    serialnum = db.Column(db.String(64))
    year = db.Column(db.Integer)
    warranty = db.Column(db.Integer)
    accounting = db.Column(db.DateTime)
    comments = db.Column(db.Text)
    buhtext = db.Column(db.String(80))
    buh_os = db.Column(db.Integer)
    check = db.Column(db.Integer)
    gas_id = db.Column(db.Integer)
    # event_id = db.Column(db.Integer)
    last_maintenance_id = db.Column(db.Integer,
                                    db.ForeignKey('maintenance_docs_db.id', ondelete='CASCADE'))
    last_maintenance = db.relationship('MaintenanceDocsDbModel', backref='hw_db', lazy='joined')

    def to_python(self):
        return dict(
            id=self.id,
            invnum=self.invnum,
            type_id=self.type_id,
            hw_type=self.hw_type.to_python(),
            legacy_user=self.legacy_user,
            empl_id=self.empl_id,
            empl_fio=self.empl_fio.to_python(),
            location=self.location,
            status_id=self.status_id,
            status=self.status.to_python(),
            manuf=self.manuf,
            model=self.model,
            vendor_id=self.vendor_id,
            serialnum=self.serialnum,
            year=self.year,
            warranty=self.warranty,
            accounting=self.accounting.strftime('%Y-%m-%d'),
            comments=self.comments,
            buhtext=self.buhtext,
            buh_os=self.buh_os,
            check=self.check,
            gas_id=self.gas_id,
            last_maintenance_id=self.last_maintenance_id,
        )

    def __repr__(self):
        return '<{}(id:{})>'.format(self.__class__.__name__, self.id)


class HwTypesModel(db.Model):
    __tablename__ = 'hw_types'

    id = db.Column(db.Integer, primary_key=True)
    hw_type = db.Column(db.String(64))
    hw_type_ru = db.Column(db.String(64))

    def to_python(self):
        return dict(
            id=self.id,
            hw_type=self.hw_type,
            hw_type_ru=self.hw_type_ru
        )


class HwStatusesModel(db.Model):
    __tablename__ = 'hw_statuses'

    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(64))
    status_name_ru = db.Column(db.String(64))

    def to_python(self):
        return dict(
            id=self.id,
            status_name=self.status_name,
            status_name_ru=self.status_name_ru,
        )
