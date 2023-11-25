from sqlalchemy.dialects.postgresql.json import JSONB

from app_setup import db


class TicketModel(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.BigInteger, primary_key=True)

    unit_id = db.Column(db.BigInteger, default=None, nullable=True)

    status_id = db.Column(db.Integer)
    docs_status_id = db.Column(db.Integer)

    subj = db.Column(db.String(80))
    body = db.Column(db.Text)
    reason = db.Column(db.String(80))
    needs_to_be_done = db.Column(db.String(120))
    comleted_work = db.Column(db.String(160))

    is_hotline = db.Column(db.Boolean, default=False)
    # hotline_status_id = db.Column(db.Integer)
    hotline_ticket_no = db.Column(db.BigInteger)
    hotline_ticket_date = db.Column(db.DateTime)
    hotline_ticket_json = db.Column(JSONB)
    hotline_fetch_date = db.Column(db.DateTime)

    iac_ticket_no = db.Column(db.BigInteger, default=None, nullable=True)
    # iac_ticket_date = db.Column(db.DateTime)

    # comments from legacy tickets
    ticket_comments_json = db.Column(JSONB)

    def to_python(self):
        hotline_ticket_date = (self.hotline_ticket_date.strftime('%Y-%m-%d')
                               if self.hotline_ticket_date else None)
        hotline_fetch_date = (self.hotline_fetch_date.strftime('%Y-%m-%d')
                              if self.hotline_fetch_date else None)
        return dict(
            id=self.id,
            unit_id=self.unit_id,
            status_id=self.status_id,
            docs_status_id=self.docs_status_id,
            subj=self.subj,
            body=self.body,
            reason=self.reason,
            needs_to_be_done=self.needs_to_be_done,
            comleted_work=self.comleted_work,
            is_hotline=self.is_hotline,
            hotline_ticket_no=self.hotline_ticket_no,
            hotline_ticket_date=hotline_ticket_date,
            hotline_ticket_json=self.hotline_ticket_json,
            hotline_fetch_date=hotline_fetch_date,
            iac_ticket_no=self.iac_ticket_no,
            ticket_comments_json=self.ticket_comments_json,
        )

    def __repr__(self):
        return '<{}(id:{})>'.format(self.__class__.__name__, self.id)
