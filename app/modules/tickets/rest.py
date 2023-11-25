import json

from flask import request
from flask.json import loads
from flask_restful import Resource

from modules.tickets.services import TicketsService


class TicketsList(Resource):
    def get(self):
        filters = json.loads(request.args.get('filters', '[]'))
        tickets = TicketsService.get_tickets_list(filters)
        return tickets

    def post(self):
        payload = loads(request.data)
        ticket = TicketsService.create(payload=payload)
        ticket_dict = ticket.to_python()
        return ticket_dict


class TicketSingle(Resource):
    def get(self, ticket_id):
        ticket = TicketsService.get_ticket_dict(ticket_id)
        return ticket

    def post(self):
        payload = loads(request.data)
        ticket = TicketsService.create(payload)
        shipment_dict = TicketsService.get_ticket_dict(ticket_id=ticket.id)
        return shipment_dict
