import json
import re

from flask import request
from flask.json import loads
from flask_restful import Resource

from modules.tickets.services import TicketsService


class TicketsList(Resource):
    def get(self):
        filters = json.loads(request.args.get('filters', '[]'))
        tickets = TicketsService.get_tickets_dicts(filters)
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


class TicketsPreviewFromExcel(Resource):
    XLSX_PATH = 'dumps/'

    ITERION_XLSX_FILENAME = '!!!_TICKETS_ITERION_2025-03-21.xlsx'
    ITERION_HEADER_ROW = 2
    # ITERION_XLSX_TAB_NO = 0  # 2025
    # ITERION_XLSX_TAB_NO = 1  # 2024
    # ITERION_XLSX_TAB_NO = 2  # 2023
    # ITERION_XLSX_TAB_NO = 3  # 2022
    # ITERION_XLSX_TAB_NO = 4  # 2021
    # ITERION_XLSX_TAB_NO = 5  # 2020
    # ITERION_XLSX_TAB_NO = 6  # 2019
    # ITERION_XLSX_TAB_NO = 7  # 2018
    ITERION_XLSX_TAB_NO = 8  # 2015-2017

    # IAC_XLSX_FILENAME = 'tickets_is_iac_2021-12-31.xlsx'
    # IAC_XLSX_FILENAME = 'tickets_is_iac_2020-12-31.xlsx'
    # IAC_XLSX_FILENAME = 'tickets_is_iac_2019-12-31.xlsx'
    # IAC_XLSX_FILENAME = 'tickets_is_iac_2018-12-31.xlsx'
    IAC_XLSX_FILENAME = 'tickets_is_iac_2017-12-31.xlsx'
    IAC_HEADER_ROWS = 3
    IAC_TICKETS_YEAR = 2017

    def get(self):
        return TicketsService.get_tickets_from_excel(
            xlsx_path=self.XLSX_PATH,
            iterion_tickets_xlsx_filename=self.ITERION_XLSX_FILENAME,
            iterion_tickets_xlsx_tab_no=self.ITERION_XLSX_TAB_NO,
            iterion_header_rows=self.ITERION_HEADER_ROW,
            iac_tickets_xlsx_filename=self.IAC_XLSX_FILENAME,
            iac_tickets_header_rows=self.IAC_HEADER_ROWS,
            iac_tickets_year=self.IAC_TICKETS_YEAR
        )


class TicketsListFormular(Resource):

    def get(self):
        filters = [
            {"field": "is_hotline", "op": "eq", "val": True},
            {"field": "iac_ticket_no", "op": "is_not_null"},
        ]
        tickets = TicketsService.get_tickets_dicts(filters)
        return tickets


class TicketsNotes(Resource):

    def get(self):
        filters = [
            {"field": "is_hotline", "op": "eq", "val": True},
            {"field": "iac_ticket_no", "op": "is_not_null"},
            {"field": "hotline_ticket_date", "op": "ge", "val": "2025-01-01"},
            {"field": "hotline_ticket_date", "op": "le", "val": "2025-12-31"},
        ]
        tickets_notes = []
        tickets = TicketsService.get_tickets(filters)
        for ticket in tickets:
            tickets_notes.append(
                dict(
                    line1='(#{}) {}'.format(ticket.hotline_ticket_no, ticket.subj),
                    line2='Пользователь: {}'.format(ticket.ticket_comments_json.get('c_m') or ''),
                    line3='',
                )
            )

        return tickets_notes
