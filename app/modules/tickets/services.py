from app_setup import db
from modules.tickets.models import TicketModel
from models.mixins import FilterMixin


class TicketsService(FilterMixin):

    @classmethod
    def get_tickets_list(cls, filters=None):
        query = TicketModel.query
        query = query.order_by(TicketModel.id.desc())
        query = cls.apply_filters(query, TicketModel, filters)
        tickets = query.all()
        tickets_list = [t.to_python() for t in tickets]

        return tickets_list

    @classmethod
    def get_ticket_dict(cls, ticket_id):
        ticket = TicketModel.query.get(ticket_id)
        if not ticket:
            return None
        ticket_dict = ticket.to_python()

        return ticket_dict

    @classmethod
    def create(cls, payload):
        ticket = TicketModel()

        ticket.unit_id = payload.get('unit_id')
        ticket.status_id = payload.get('status_id')
        ticket.docs_status_id = payload.get('docs_status_id')
        ticket.subj = payload.get('subj')
        ticket.body = payload.get('body')
        ticket.reason = payload.get('reason')
        ticket.needs_to_be_done = payload.get('needs_to_be_done')
        ticket.comleted_work = payload.get('comleted_work')
        ticket.is_hotline = payload.get('is_hotline')
        ticket.hotline_ticket_no = payload.get('hotline_ticket_no')
        ticket.hotline_ticket_date = payload.get('hotline_ticket_date')
        ticket.hotline_ticket_json = payload.get('hotline_ticket_json')
        ticket.hotline_fetch_date = payload.get('hotline_fetch_date')
        ticket.iac_ticket_no = payload.get('iac_ticket_no')
        ticket.ticket_comments_json = payload.get('ticket_comments_json')

        db.session.add(ticket)
        db.session.commit()

        return ticket
