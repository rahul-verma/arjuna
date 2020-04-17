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

class PytestHooks:
    '''
        Easy hooks to be used in `pytest` configuration file: `conftest.py` placed under `<Project_Root_Dir/test` directory in test project.
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

            To be used in `pytest_runtest_makereport` hook in `conftest.py`.

            Args:
                item: `pytest`'s Item object
                result: `pytest`'s TestReport object.

            Keyword Arguments:
                ignore_passed: (Optional) If set to True, screenshot is taken when the test function completes. Default is True.
                ignore_fixtures: (Optional) If set to True, screenshot is not taken for test fixture functions. Default is False.

            Note:
                - For taking the screenshot, it does a look up for a `screen_shooter` attribute in the object spaces in following order:
                    - Function Space
                    - Module Space
                    - Session Space

                - The screen_shooter attribute should contain a `ScreenShooter` i.e. an object of a class that inherits from ScreenShooter class and completes its protocol.
                
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


    def delegate(metafunc):
        from arjuna import Arjuna
        from arjuna.tpi.engine.data.markup import record

        if hasattr(metafunc.function, '_delegate') and metafunc.function._delegate is True:
            delegated_fix_names = [f for f in metafunc.fixturenames if f not in {'request', 'data'}]
            run_configs = Arjuna.get_run_configs()
            ids = ["RunConfig: {} ".format(c.name) for c in run_configs]

            if len(delegated_fix_names) == 1:
                argvalues = [record(run_config=c).build().all_records[0] for c in run_configs]
                try:
                    metafunc.parametrize(",".join(delegated_fix_names), argvalues=argvalues, ids=ids, indirect=True)
                except ValueError as e:
                    raise Exception("Exception in delegation logic. Most likely you have an already parameterized fixture. You can not use a data driven fixture in an auto-delegated test. Test Function: {}.".format(metafunc.function))

            else:
                argvalues = []
                for c in run_configs:
                    argvalues.append([record(run_config=c).build().all_records[0] for i in delegated_fix_names])
                try:
                    metafunc.parametrize(",".join(delegated_fix_names), argvalues=argvalues, ids=ids, indirect=True)
                except ValueError as e:
                    raise Exception("Exception in delegation logic. Most likely you have an already parameterized fixture. You can not use a data driven fixture in an auto-delegated test. Test Function: {}.".format(metafunc.function))