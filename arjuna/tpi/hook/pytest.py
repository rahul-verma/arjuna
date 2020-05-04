# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from itertools import cycle

class PytestHooks:
    '''
        Easy hooks to be used in **pytest** configuration file: **conftest.py** placed under **<Project_Root_Dir/test** directory in test project.
    '''

    @classmethod
    def _get_request_attr(cls, item, obj_name):
        from .test import Space
        request =  cls._get_request_obj(item)
        res = Space(request)
        return getattr(res, obj_name)

    @classmethod
    def _get_request_obj(cls, item):
        return item.funcargs['request']

    @classmethod
    def _get_plugin(cls, item, name):
        return item.config.pluginmanager.getplugin(name)

    @classmethod
    def _get_html_report_plugin(cls, item):
        return cls._get_plugin(item, 'html')

    @classmethod
    def _get_screen_shooter(cls, item):
        try:
            return getattr(item.function, "screen_shooter")
        except:
            try:
                return getattr(item.module, "screen_shooter")
            except:
                return getattr(item.session, "screen_shooter")

    @classmethod
    def add_screenshot_for_result(cls, item, result, *, ignore_passed=True, ignore_fixtures=False):
        '''
            Automatically add screenshot to HTML Report File.

            To be used in **pytest_runtest_makereport** hook in **conftest.py**.

            Args:
                item: **pytest**'s Item object
                result: **pytest**'s TestReport object.

            Keyword Arguments:
                ignore_passed: (Optional) If set to True, screenshot is taken when the test function completes. Default is True.
                ignore_fixtures: (Optional) If set to True, screenshot is not taken for test fixture functions. Default is False.

            Note:
                - For taking the screenshot, it does a look up for a **screen_shooter** attribute in the object spaces in following order:
                    - Function Space
                    - Module Space
                    - Session Space

                - The screen_shooter attribute should contain a **ScreenShooter** i.e. an object of a class that inherits from ScreenShooter class and completes its protocol.
                
                - This is a lenient hook. This means that if any exception happens in it, it ignores the exception and logs a warning message.
        '''

        try:
            try:
                screen_shooter = cls._get_screen_shooter(item)
            except AttributeError:
                return

            html_plugin = cls._get_html_report_plugin(item)
            pytest_html = html_plugin
            report = result.get_result()
            extra = getattr(report, 'extra', [])

            if ignore_fixtures:
                if report.when == 'call':
                    return

            xfail = hasattr(report, 'wasxfail')

            if ignore_passed and report.passed:
                return
            # if (report.skipped and xfail) and (report.failed and not xfail):
                # extra.append(pytest_html.extras.url(app.url))


            import re
            rname = re.sub(r"\[.*?\]", "", report.nodeid)
            image = screen_shooter.take_screenshot(prefix=rname)
            fpath = "../screenshot/{}".format(image.file_name)
            img_elem = '''<img src="data:image/png;base64,{}"/>'''.format(image.base64)
            extra.append(
                pytest_html.extras.html(
                    '''<div class="image"><a href="{}" target="_blank">{}</a>'''.format(fpath, img_elem)
                )
            )
            report.extra = extra
        except Exception as e:
            from arjuna import log_warning
            log_warning("Error in add_screenshot_for_result hook: " + str(e))


    @classmethod
    def configure_group_for_test(cls, metafunc):
        '''
            Configures **group** fixture for a test.

            Acts only if **group** fixture is present in the signature of a test function or signature(s) of any of its fixture(s) in its fixture hierarchy. 

            To be used in **pytest_generate_tests** hook in **conftest.py**.

            Args:
                metafunc: **pytest**'s MetaFunc object

            Note:
                The **group** fixture yields a **DataRecord** object containing the following keys:
                    - **name**: Group name
                    - **config**: **Configuration** object assigned to the group.
                    - **thread_name**: Thread name for the thread in which the Test Group is running.
        '''

        from arjuna import Arjuna, ArjunaOption, log_debug, C
        from arjuna.tpi.engine.data.markup import record
        log_debug("{} {}".format(metafunc.function, metafunc.fixturenames))

        group_params = Arjuna.get_group_params()
        conf = None
        m = metafunc.function.__module__
        group = record(**group_params).build(context='Group').all_records[0]
        log_debug("Parameterizing distributor for module: {} with group: {}".format(m, group))
        metafunc.parametrize("group", argvalues=[group], ids=["G"], indirect=True)

    @classmethod
    def select_tests(cls, pytest_items, pytest_config):
        '''
            Select tests from items collected by pytest, based on Arjuna rules.

            Arguments:
                pytest_items: List of pytest `Item` objects. Each item represents a collected test function node.
                pytest_config: pytest Config object
        '''
        from arjuna import Arjuna
        from arjuna.core.error import ExclusionRuleMet, NoInclusionRuleMet
        selector = Arjuna.get_test_selector()
        final_selection = []
        deselected = []
        for item in pytest_items:
            qual_name = item.nodeid.split('::')[0].replace("/",".").replace('\\',"").replace(".py","") + "." + item.name.split("[")[0]
            try:
                selector.validate(Arjuna.get_test_meta_data(qual_name))
            except (ExclusionRuleMet, NoInclusionRuleMet) as e:
                deselected.append(item)
            else:
                final_selection.append(item)

        if deselected:
            pytest_config.hook.pytest_deselected(items=deselected)
            pytest_items[:] = final_selection


        