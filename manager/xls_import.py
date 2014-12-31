#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

import xlrd
from py3compat import text_type

logger = logging.getLogger(__name__)


def handle_xls_file(fpath, handle_row, **kwargs):
    try:
        wb = xlrd.open_workbook(fpath)
        ws = wb.sheets()[0]
    except:
        raise ValueError("Not an Excel file")

    row_num = 1
    empty = 0

    def val_from(row, index):
        raw = ws.row_values(row)[index]
        if isinstance(raw, (float, int)):
            d = text_type(int(raw))
        else:
            d = text_type(raw)
        return d

    while row_num:
        print(row_num)
        try:
            number = val_from(row_num, 0)
        except:
            number = ''
        try:
            name = val_from(row_num, 1)
        except:
            name = ''
        row_num += 1
        if not number.strip():
            if empty > 10:
                row_num = None
                break
            empty += 1
            continue
        else:
            empty = 0
        handle_row(number, name, **kwargs)
    return
