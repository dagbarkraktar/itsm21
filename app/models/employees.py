from app_setup import db


class EmplListGasModel(db.Model):
    __tablename__ = 'empl_list_gas'

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(128))
    tab_no = db.Column(db.String(128))
    depts = db.Column(db.String(256))
    post = db.Column(db.String(256))
    post_dop = db.Column(db.String(256))
    date_recr = db.Column(db.DateTime)
    date_post = db.Column(db.DateTime)
    sx = db.Column(db.String(16))
    date_birth = db.Column(db.DateTime)

    def to_python(self):
        return dict(
            id=self.id,
            fio=self.fio,
            depts=self.depts,
            post=self.post,
            post_dop=self.post_dop,
        )
