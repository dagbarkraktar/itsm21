from datetime import datetime, timezone

from app_setup import db


class MaintenanceRecordModel(db.Model):
    """
    Record of maintenance performed
    """
    __tablename__ = 'maintenance_records'
    id = db.Column(db.BigInteger, primary_key=True)

    hw_id = db.Column(db.BigInteger, db.ForeignKey('hw_db.id', ondelete='CASCADE'), nullable=False)
    # back_populates is more clearly for two directional relations
    hardware = db.relationship('HwDbModel', back_populates='maintenance_records')

    doc_id = db.Column(db.BigInteger, db.ForeignKey('maintenance_docs.id', ondelete='CASCADE'), nullable=False)
    doc = db.relationship('MaintenanceDocModel', backref='maintenance_records', lazy='joined')

    # service notes (repairs needed, etc)
    notes = db.Column(db.Text)

    # metadata
    created_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )

    def to_python(self):
        return dict(
            id=self.id,
            hw_id=self.hw_id,
            hardware=self.hardware.to_python(),
            doc_id=self.doc_id,
        )


class MaintenanceDocModel(db.Model):
    __tablename__ = 'maintenance_docs'

    id = db.Column(db.BigInteger, primary_key=True)

    # maintenance period
    quarter = db.Column(db.Integer, nullable=False)  # Квартал (1-4)
    year = db.Column(db.Integer, nullable=False)  # Год проведения

    # year = db.Column(db.Integer)
    # num_thru_year = db.Column(db.Integer)  # maintenance number over the year (1,2,3,4)

    # maintenance  info
    doc_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    # performed_by_id = db.Column(db.Integer, db.ForeignKey('empl_list_gas.id', ondelete='CASCADE'))
    # performed_by = db.relationship('EmplListGasModel', backref='performed_maintenance', lazy='joined')

    # doc_date = db.Column(db.DateTime)
    # doc_num = db.Column(db.String(16))
    planned_units_qty = db.Column(db.Integer)
    # units_id_list = db.Column(db.String(2048))
