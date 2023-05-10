from app_setup import db


class HwDbModel(db.Model):
    __tablename__ = "hw_db"

    id = db.Column(db.BigInteger, primary_key=True)
    invnum = db.Column(db.String(12))
    type_id = db.Column(db.Integer, db.ForeignKey("hw_types.id", ondelete='CASCADE'))
    hw_type = db.relationship("HwTypesModel", backref="hw_db", lazy="joined")
    legacy_user = db.Column(db.String(50))
    empl_id = db.Column(db.Integer, db.ForeignKey("empl_list_gas.id", ondelete='CASCADE'))
    empl_fio = db.relationship("EmplListGasModel", backref="hw_db", lazy="joined")
    location = db.Column(db.String(4))
    status_id = db.Column(db.Integer, db.ForeignKey("hw_statuses.id", ondelete='CASCADE'))
    status = db.relationship("HwStatusesModel", backref="hw_db", lazy="joined")
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
                                    db.ForeignKey("maintenance_docs_db.id", ondelete='CASCADE'))
    last_maintenance = db.relationship("MaintenanceDocsDbModel", backref="hw_db", lazy="joined")


class HwTypesModel(db.Model):
    __tablename__ = "hw_types"

    id = db.Column(db.Integer, primary_key=True)
    hw_type = db.Column(db.String(64))
    hw_type_ru = db.Column(db.String(64))


class HwStatusesModel(db.Model):
    __tablename__ = "hw_statuses"

    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(64))
    status_name_ru = db.Column(db.String(64))
