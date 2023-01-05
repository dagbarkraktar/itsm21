from main import db


class MaintenanceDocsDbModel(db.Model):
    __tablename__ = "maintenance_docs_db"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    num_thru_year = db.Column(db.Integer)  # maintenance number over the year (1,2,3,4)
    doc_date = db.Column(db.DateTime)
    doc_num = db.Column(db.String(16))
    units_qty = db.Column(db.Integer)
    units_id_list = db.Column(db.String(2048))


class MaintenanceDbModel(db.Model):
    __tablename__ = "maintenance_db"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer)
    hw_unit_id = db.Column(db.Integer)
    status_id = db.Column(db.Integer)
