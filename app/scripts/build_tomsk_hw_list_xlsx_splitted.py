#
# Export hardware list to xlsx for load to new IS IAC
# table splitted by ref HwTomskModels
#

import arrow
import xlsxwriter

from app_setup import db, create_app
from modules.hwdb.services import HwUnitsService


XLSX_PATH = '../dumps/'
XLSX_NAME = 'tomsk_hw_list_splitted'
XLSX_EXT = 'xlsx'

OBJECT_CODE = '32OS0000'
OBJECT_TITLE = 'Брянский областной суд'

TITLE_COMPLECT_UNIT = '1 Отдельно стоящая на учете единица ТС'
TITLE_COMPLECT_ARM = '2 Комплект АРМ'

TYPE_MAP = {
    3: TITLE_COMPLECT_ARM,
    27: TITLE_COMPLECT_ARM,
    28: TITLE_COMPLECT_ARM,
    4: TITLE_COMPLECT_UNIT,
    8: TITLE_COMPLECT_UNIT,
    6: TITLE_COMPLECT_UNIT,
    9: TITLE_COMPLECT_UNIT,
    5: TITLE_COMPLECT_UNIT,
    30: TITLE_COMPLECT_UNIT,
    34: TITLE_COMPLECT_UNIT,
    35: TITLE_COMPLECT_UNIT,
}

BUH_OS_MAP = {
    1: 'Программно-техническое средство Балансодержателя',
    3: 'Основное средство ФГБУ ИАЦ Судебного департамента',
}

WARRANTY_MAP = {
    1: 12,
    3: 36,
}

HW_SB_TYPE = 3


def main():
    ts = arrow.utcnow().to('Europe/Moscow').strftime('%Y-%m-%d-%H.%M.%S.%f')
    workbook = xlsxwriter.Workbook(f'{XLSX_PATH}{XLSX_NAME}_{ts}.{XLSX_EXT}')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, f'TOMSK EXPORT {ts}')

    filters = [
        {'field': 'status_id', 'op': 'not_in', 'val': [7, 8, 9]},
        {'field': 'type_id', 'op': 'in', 'val': [3, 27, 28, 4, 8, 6, 9, 5, 30, 34, 35]},
        {'field': 'buh_os', 'op': 'in', 'val': [1, 3]},
    ]
    hw_units = HwUnitsService.get_hw_units_list(filters)

    cur_row = 1
    unknown_manuf_models = []
    for unit in hw_units:
        invnum = unit.get('invnum')
        type_id = unit.get('type_id')
        buh_os = unit.get('buh_os')
        accounting = unit.get('accounting')
        manuf = unit.get('manuf')
        model = unit.get('model')
        line = [
            OBJECT_CODE,
            OBJECT_TITLE,
            TYPE_MAP[type_id],
            unit.get('hw_type', {}).get('hw_type_tomsk'),
            manuf,
            model,
            unit.get('serialnum'),
            invnum,
            BUH_OS_MAP[buh_os]
        ]
        accounting_date = arrow.get(accounting).strftime('%d.%m.%Y') if accounting else ''
        line.append(check_acc_date(invnum, accounting_date))
        line.append(WARRANTY_MAP[buh_os])
        line.append('Рабочее')
        line.append(unit.get('buhtext'))

        # check if our manuf/model in tomsk ref
        tomsk_filters = [
            {'field': 'manuf', 'op': 'eq', 'val': manuf},
            {'field': 'model', 'op': 'eq', 'val': model},
        ]
        tomsk_units_from_ref = HwUnitsService.get_hw_tomsk_models_list(filters=tomsk_filters)
        if tomsk_units_from_ref:
            for col, val in enumerate(line):
                worksheet.write(cur_row, col, val)
            cur_row += 1
        else:
            unknown_manuf_models.append(line)

    # write unknown manuf/models after 4 lines gap
    cur_row += 4
    for u_line in unknown_manuf_models:
        for col, val in enumerate(u_line):
            worksheet.write(cur_row, col, val)
        cur_row += 1

    workbook.close()


def check_acc_date(invnum: str, acc_date: str) -> str:
    if acc_date == '21.01.1999':
        # fix accounting stub date (used in legacy monitors/ups complect)
        sblock = HwUnitsService.get_by_invnum_n_type(
            invnum=invnum,
            type_id=HW_SB_TYPE
        )
        accounting = sblock.accounting
        fixed_acc_date = (
            arrow.get(accounting).strftime('%d.%m.%Y') if accounting else ''
        )
        return fixed_acc_date

    return acc_date


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        main()
