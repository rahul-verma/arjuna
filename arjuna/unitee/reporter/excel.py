'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import threading
import sys
import xlwt

from collections import OrderedDict
from arjuna.lib.thread.decorators import *
from arjuna.unitee.reporter.result.types import SteppedResult
from arjuna.unitee.enums import *

# The autofit solution has been taken from StackOverflow thread
# https://stackoverflow.com/questions/6929115/python-xlwt-accessing-existing-cell-content-auto-adjust-column-width
class _ExcelSheet:

    def __init__(self, wb, name):
        self.__wb = wb
        self.__name = name
        self.__current_row_counter = -1
        self.ws = self.__wb.add_sheet(self.__name)
        self.__header_style = xlwt.easyxf('font: bold on; borders: left thin, right thin, top thin, bottom thin; align: vertical top;\
                                          pattern: pattern solid, fore_colour coral;')
        self.__row_style = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; align: vertical top')
        self.__row_style.alignment.wrap = 1
        self.__widths = dict()

    def __write_row(self, data, style):
        import arial10
        self.__current_row_counter += 1
        for index, item in enumerate(data):
            item = str(item)
            self.ws.write(self.__current_row_counter, index, item, style)
            width = int(arial10.fitwidth(item))
            if width > self.__widths.get(index,0):
                self.__widths[index] = width
                self.ws.col(index).width = width

    def update_headers(self, headers):
        self.__write_row(headers, self.__header_style)

    def update_entry(self, record):
        self.__write_row(record, self.__row_style)

class ExcelReporter:

    def __init__(self):
        self.lock = threading.RLock()
        self.path = ArjunaCore.config.value(UniteePropertyEnum.RUN_REPORT_DIR) + "/ArjunaTestReport.xls"

    def set_up(self):
        self.wb = xlwt.Workbook()
        self.info_sheet = _ExcelSheet(self.wb, "Notifications")
        self.exec_sheet = _ExcelSheet(self.wb, "Execution Report")
        self.steps_sheet = _ExcelSheet(self.wb, "Steps")
        self.issues_sheet = _ExcelSheet(self.wb, "Issues")
        self._execheaders = None

    def tear_down(self):
        self.wb.save(self.path)

    def update_info_headers(self, headers):
        self.info_sheet.update_headers(headers)

    def update_execution_headers(self, headers):
        self.exec_sheet.update_headers(headers)
        self._execheaders = headers

    def update_step_headers(self, headers):
        self.steps_sheet.update_headers(list(self._execheaders)[:10] + list(headers))

    def update_issue_headers(self, headers):
        self.issues_sheet.update_headers(headers)

    @sync_method('lock')
    def _update(self, sheet, record):
        sheet.update_entry(record)

    def update_info(self, rdict):
        self._update(self.info_sheet, rdict.values())

    def update_issue(self, issue):
        self._update(self.issues_sheet, issue.values())

    @sync_method('lock')
    def update_test_object_result(self, reportable):
        self._update(self.exec_sheet, reportable.result.values())
        if reportable.has_steps():
            first = True
            prefix = ["-" for i in range(10)]
            for step in reportable.steps:
                try:
                    if first:
                        self._update(self.steps_sheet, list(reportable.result.values())[:10] + list(step.values()))
                        first=False
                    else:
                        self._update(self.steps_sheet, prefix + list(step.values()))
                except Exception as e:
                    print ("Exception occured")
                    print (e)
                    import traceback
                    traceback.print_exc()
                    sys.exit(1)
