#
# Export hardware list to xlsx for load to new IS IAC
#

import arrow
import xlsxwriter

from app_setup import db, create_app
from modules.hwdb.services import HwUnitsService

XLSX_PATH = '../dumps/'
XLSX_NAME = 'tomsk_hw_list'
XLSX_EXT = 'xlsx'

OBJECT_CODE = '32OS0000'
OBJECT_TITLE = 'Брянский областной суд'

TYPE_MAP = {
    3: 'Комплект АРМ',
    27: 'Комплект АРМ',
    28: 'Комплект АРМ',
    4: 'Отдельно стоящая на учете единица ТС',
    8: 'Отдельно стоящая на учете единица ТС',
    6: 'Отдельно стоящая на учете единица ТС',
    9: 'Отдельно стоящая на учете единица ТС',
    5: 'Отдельно стоящая на учете единица ТС',
    30: 'Отдельно стоящая на учете единица ТС',
    34: 'Отдельно стоящая на учете единица ТС',
    35: 'Отдельно стоящая на учете единица ТС',
}

BUH_OS_MAP = {
    1: 'Программно-техническое средство Балансодержателя',
    3: 'Основное средство ФГБУ ИАЦ Судебного департамента',
}

WARRANTY_MAP = {
    1: 12,
    3: 36,
}


def main():
    ts = arrow.utcnow().to('Europe/Moscow').strftime('%Y-%m-%d-%H.%M.%S.%f')
    workbook = xlsxwriter.Workbook(f'{XLSX_PATH}{XLSX_NAME}_{ts}.{XLSX_EXT}')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, f'TOMSK EXPORT {ts}')
    cur_row = 1

    filters = [
        {'field': 'status_id', 'op': 'not_in', 'val': [7, 8, 9]},
        {'field': 'type_id', 'op': 'in', 'val': [3, 27, 28, 4, 8, 6, 9, 5, 30, 34, 35]},
        {'field': 'buh_os', 'op': 'in', 'val': [1, 3]},
    ]
    hw_units = HwUnitsService.get_hw_units_list(filters)

    previous_dt = '21.01.1999'
    for unit in hw_units:
        type_id = unit.get('type_id')
        buh_os = unit.get('buh_os')
        accounting = unit.get('accounting')

        worksheet.write(cur_row, 0, OBJECT_CODE)
        worksheet.write(cur_row, 1, OBJECT_TITLE)
        worksheet.write(cur_row, 2, TYPE_MAP[type_id])
        worksheet.write(cur_row, 3, unit.get('hw_type', {}).get('hw_type_tomsk'))
        worksheet.write(cur_row, 4, unit.get('manuf'))
        worksheet.write(cur_row, 5, unit.get('model'))
        worksheet.write(cur_row, 6, unit.get('serialnum'))
        worksheet.write(cur_row, 7, unit.get('invnum'))
        worksheet.write(cur_row, 8, BUH_OS_MAP[buh_os])

        # fix accounting dt stub value (used in legacy monitors/ups complect)
        accounting_dt = arrow.get(accounting).strftime('%d.%m.%Y') if accounting else ''
        if accounting_dt == '21.01.1999':
            accounting_dt = previous_dt
        previous_dt = accounting_dt
        worksheet.write(cur_row, 9, accounting_dt)

        worksheet.write(cur_row, 10, WARRANTY_MAP[buh_os])
        worksheet.write(cur_row, 11, 'Рабочее')
        worksheet.write(cur_row, 12, unit.get('buhtext'))

        cur_row += 1

    workbook.close()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        main()
