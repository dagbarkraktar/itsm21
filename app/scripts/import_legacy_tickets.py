#
# One time db seed: Load legacy tickets from iterion xlsx to db
#
import re

import arrow
import openpyxl

from app_setup import db, create_app
from modules.tickets.models import TicketModel
from modules.tickets.services import TicketsService
from modules.hwdb.services import HwUnitsService

XLSX_PATH = '../dumps/'

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

# table with iac tickets to match with iterion tickets
IAC_XLSX_FILENAME = 'tickets_is_iac_2017-12-31.xlsx'
IAC_HEADER_ROWS = 3
IAC_TICKETS_YEAR = 2017


def main():
    app = create_app()

    tickets_from_excel = TicketsService.get_tickets_from_excel(
        xlsx_path=XLSX_PATH,
        iterion_tickets_xlsx_filename=ITERION_XLSX_FILENAME,
        iterion_tickets_xlsx_tab_no=ITERION_XLSX_TAB_NO,
        iterion_header_rows=ITERION_HEADER_ROW,
        iac_tickets_xlsx_filename=IAC_XLSX_FILENAME,
        iac_tickets_header_rows=IAC_HEADER_ROWS,
        iac_tickets_year=IAC_TICKETS_YEAR
    )

    lines_w_failed_units = []
    line_no = 1 + ITERION_HEADER_ROW
    for ticket_dict in tickets_from_excel:
        body = ticket_dict.get('body')
        b_serialnum = ''
        if body:
            match = re.search(r'Заводской номер: \S+', body)
            b_serialnum = match[0][17:] if match else None
        with app.app_context():
            # check if ticket already exist
            hotline_ticket_no = ticket_dict.get("hotline_ticket_no")
            ticket_subj = ticket_dict.get('subj')
            hotline_ticket_date = arrow.get(
                ticket_dict.get("hotline_ticket_date"),
                'DD-MM-YYYY'
            ).datetime
            ticket_db = TicketModel.query.filter(
                TicketModel.hotline_ticket_no == hotline_ticket_no,
                TicketModel.subj == ticket_subj,
                TicketModel.hotline_ticket_date == hotline_ticket_date
            ).first()
            if ticket_db:
                print('SKIP, ALREADY EXIST!!! ({} - {} - {})'.format(
                    hotline_ticket_no,
                    hotline_ticket_date.strftime('%d.%m.%y'),
                    ticket_subj,))
                continue

            unit = HwUnitsService.get_by_invnum_n_serial(invnum=None, serialnum=b_serialnum)
            if not unit:
                lines_w_failed_units.append(line_no)

            ticket = TicketModel()
            ticket.unit_id = unit.id if unit else None
            ticket.subj = ticket_dict.get('subj')
            ticket.body = ticket_dict.get('body')
            ticket.comleted_work = ticket_dict.get('comleted_work')

            hotline_ticket_no = ticket_dict.get("hotline_ticket_no")
            ticket.hotline_ticket_no = hotline_ticket_no
            ticket.is_hotline = True if hotline_ticket_no else False
            ticket.iac_ticket_no = ticket_dict.get("iac_ticket_no")
            hotline_ticket_date = arrow.get(
                ticket_dict.get("hotline_ticket_date"),
                'DD-MM-YYYY'
            ).datetime
            ticket.hotline_ticket_date = hotline_ticket_date

            ticket.ticket_comments_json = ticket_dict.get("comments")

            db.session.add(ticket)
            db.session.commit()

            print('{} ======================================================================='.format(line_no))
            print(f'SN: {b_serialnum}')
            print(f'HW: {unit}')
            print(f'{hotline_ticket_no} / {ticket.iac_ticket_no} - {ticket_dict.get("hotline_ticket_date")} ({hotline_ticket_date})')
            print(f'SUBJ: {ticket_dict.get("subj")}')
            # print(f'BODY: {ticket_dict.get("body")}')
            # print(f'COMPLETED: {ticket_dict.get("comleted_work")}')
            # print(f'COMMENTS: {ticket_dict.get("comments")}')
            line_no += 1

    print(f'Lines processed: {line_no-ITERION_HEADER_ROW-1}')
    print(f'Lines w/failed units: {lines_w_failed_units}')


if __name__ == '__main__':
    main()
