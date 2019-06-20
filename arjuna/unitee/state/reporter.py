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

import os
import abc
import threading

from arjuna.lib.utils import file_utils
from arjuna.unitee.enums import *
from arjuna.lib.thread.decorators import *
from arjuna.unitee.reporter.mcr import *
from arjuna.unitee.reporter.cr import *
from arjuna.unitee.reporter.excel import *

from arjuna.tpi.enums import ArjunaOption

class __Reporter(metaclass=abc.ABCMeta):
    def __init__(self):
        self.__reporters = []

    @property
    def reporters(self):
        return self.__reporters

    def _add_reporter(self, reporter):
        self.reporters.append(reporter)

    def set_up(self):
        for reporter in self.reporters:
            reporter.set_up()

    def tear_down(self):
        for reporter in self.reporters:
            reporter.tear_down()

class NonActiveReporter(__Reporter, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def generate(self):
        pass

class OfflineReporter(NonActiveReporter):
    def __init__(self):
        super().__init__()

    def generate(self):
        pass

class DeferredReporter(NonActiveReporter):
    def __init__(self, rr_dir):
        super().__init__()
        self.__rr_dir = rr_dir
        deferred_formats = Arjuna.get_central_config().get_arjuna_option_value(ArjunaOption.UNITEE_PROJECT_DEFERRED_REPORTERS).as_enum_list(DeferredReporterNames)
        for rfmt in deferred_formats:
            if rfmt == DeferredReporterNames.EXCEL:
                rdir = os.path.join(self.__rr_dir, "/excel")
                os.makedirs(rdir)
                self._add_reporter(ExcelReporter(rdir))
            else:
                raise Exception("{} deffered reporting not implemented yet.".format(rfmt))

    def generate(self):
        pass

class ActiveReporter(__Reporter):

    def __init__(self):
        super().__init__()
        self.lock = threading.RLock()
        rdir = Arjuna.get_central_config().get_arjuna_option_value(ArjunaOption.REPORT_DIR).as_string()
        file_utils.delete_dir_if_exists(rdir)
        self.__rr_dir = Arjuna.get_central_config().get_arjuna_option_value(ArjunaOption.UNITEE_PROJECT_RUN_REPORT_DIR).as_string()
        os.makedirs(self.__rr_dir)

    def set_up(self):
        active_formats = Arjuna.get_central_config().get_arjuna_option_value(
            ArjunaOption.UNITEE_PROJECT_ACTIVE_REPORTERS).as_enum_list(ActiveReporterNames)
        for afmt in active_formats:
            if afmt == ActiveReporterNames.MIN_CONSOLE:
                self._add_reporter(MinimalConsoleReporter())
            elif afmt == ActiveReporterNames.CONSOLE:
                self._add_reporter(ConsoleReporter())
            elif afmt == ActiveReporterNames.EXCEL:
                self._add_reporter(ExcelReporter())
            else:
                raise Exception("{} active reporting not implemented yet.".format(afmt))
        super().set_up()
        for reporter in self.reporters:
            reporter.update_info_headers([i.name for i in InfoEntryEnum])
            reporter.update_execution_headers([i.name for i in ResultEntryEnum])
            reporter.update_step_headers([i.name for i in StepEntryEnum])
            reporter.update_issue_headers([i.name for i in IssueEntryEnum])

    @sync_method('lock')
    def update_info(self, reportable):
        for reporter in self.reporters:
            reporter.update_info(reportable.get_dict())

    @sync_method('lock')
    def update_result(self, reportable):
        if reportable.has_issues():
            for issue in reportable.issues:
                for reporter in self.reporters:
                    reporter.update_issue(issue.get_dict())
        for reporter in self.reporters:
            reporter.update_test_object_result(reportable.get_reportable())

    def report(self, offline=False):
        dr = DeferredReporter(self.__rr_dir)
        dr.set_up()
        dr.generate()
        dr.tear_down()

    def archive(self):
        import shutil
        shutil.copytree(self.__rr_dir,
                        os.path.join(
                            ArjunaCore.config.value(UniteePropertyEnum.ARCHIVES_DIR),
                            ArjunaCore.config.value(UniteePropertyEnum.IRUNID)
                        ))