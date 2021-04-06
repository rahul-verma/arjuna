# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

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

import os

from itertools import cycle
from py.xml import html, raw

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
    def _get_protocol_object(cls, item, name):
        try:
            return getattr(item.function, name)
        except:
            try:
                return getattr(item.module, name)
            except:
                return getattr(item.session, name)

    @classmethod
    def prepare_result(cls, result):
        report = result.get_result()
        import re
        if report.sections:
            for index, content in enumerate(report.sections) :
                name = content[0]
                if "stderr" in name:
                    if "Logging error" in content[1]:
                        revised = re.sub(r"--- Logging error ---.*?Arguments.*?\)\n" , f"\n", content[1], flags=re.S)
                        revised = revised.strip()
                        if revised :
                            report.sections[index] = (name, revised.strip())
                        else:
                            report.sections[index] = (name, "NA")

    @classmethod
    def inject_arjuna_js(cls, prefix):
        from arjuna import C
        with open(C("arjuna.root.dir") + "/arjuna/res/arjuna.js", "r") as f:
            prefix += [html.script(raw(f.read()))]
        with open(C("arjuna.root.dir") + "/arjuna/res/arjuna.html", "r") as f:
            prefix += [raw(f.read())]

    @classmethod
    def set_report_title(cls, report):
        from arjuna import C
        report.title = "{} Automated Test Report".format(C("project.name").title())

    @classmethod
    def add_env_data(cls, config):
        from arjuna import C, Arjuna
        import pkg_resources
        config._metadata['Arjuna Version'] = pkg_resources.require("arjuna")[0].version
        config._metadata['Arjuna Test Project Directory'] = C("project.root.dir")
        config._metadata['Arjuna Test Project Name'] = C("project.name")
        config._metadata['Reference Configuration'] = Arjuna.get_config().name
        config._metadata['Pytest Command (Converted)'] = Arjuna.get_pytest_command_for_group()
        config._metadata['Pytest Command (Provided)'] = Arjuna._get_command()

    @classmethod
    def enhance_reports(cls, item, result):
        '''
            Automatically add screenshot to HTML Report File.

            To be used in **pytest_runtest_makereport** hook in **conftest.py**.

            Args:
                item: **pytest**'s Item object
                result: **pytest**'s TestReport object.

            Note:
                - For taking the screenshot, it does a look up for a **screen_shooter** attribute in the object spaces in following order:
                    - Function Space
                    - Module Space
                    - Session Space

                - The screen_shooter attribute should contain a **ScreenShooter** i.e. an object of a class that inherits from ScreenShooter class and completes its protocol.
                
                - This is a lenient hook. This means that if any exception happens in it, it ignores the exception and logs a warning message.
        '''

        try:
            from arjuna import Arjuna, ArjunaOption, log_debug
            ignore_passed_for_screenshots = not Arjuna.get_config().value(ArjunaOption.REPORT_SCREENSHOTS_ALWAYS)
            ignore_passed_for_network = not Arjuna.get_config().value(ArjunaOption.REPORT_NETWORK_ALWAYS)

            include_images = True
            include_network = True

            html_plugin = cls._get_html_report_plugin(item)
            pytest_html = html_plugin
            report = result.get_result()

            log_debug("Node ID: {}".format(report.nodeid), contexts="report")
            log_debug("Stage: {}".format(report.when), contexts="report")

            extra = getattr(report, 'extra', [])

            # if ignore_fixtures:
            #     if report.when == 'call':
            #         return

            xfail = hasattr(report, 'wasxfail')

            if ignore_passed_for_screenshots and report.passed:
                include_images = False
            else:
                # if (report.skipped and xfail) and (report.failed and not xfail):
                    # extra.append(pytest_html.extras.url(app.url))
                try:
                    screen_shooter = cls._get_protocol_object(item, "screen_shooter")
                except AttributeError:
                    pass
                else:
                    try:
                        screen_shooter.take_screenshot(prefix=report.nodeid)
                    except Exception:
                        # any error in auto-screen shot is ignored.
                        pass

            log_debug("Attempting to get network_recorder from request", contexts="report")
            try:
                network_recorder = cls._get_protocol_object(item, "network_recorder")
            except AttributeError as e:
                log_debug("No network_recorder", contexts="report")
            else:
                try:
                    log_debug("Registering traffic", contexts="report")
                    network_recorder.register()
                    log_debug("Traffic registered.", contexts="report")
                except Exception as e:
                    log_debug("Exception in registering network traffic: " + str(e), contexts="report")

            if ignore_passed_for_network and report.passed:
                include_network = False

            log_debug("Include images {}".format(include_images), contexts="report")
            log_debug("Include network {}".format(include_network), contexts="report")

            # When this place is reached by a resource that failed/erred or a test (irrespective of result)
            if (report.when in {"setup", "teardown"} and not report.passed) or report.when =="call":
                test_container = Arjuna.get_report_metadata()
                if test_container.has_content():
                    log_debug("Extra Content Found for HTML Report", contexts="report")
                    extra_html = test_container.as_report_html(include_images=include_images, include_network=include_network)
                    if extra_html:
                        extra.append(pytest_html.extras.html(extra_html))
                        report.extra = extra

            # For fixtures with errors, failures, clean the resources.
            if report.when in {"setup", "teardown"}:
                if not report.passed:
                    log_debug("Clearing report extras.", contexts="report")
                    Arjuna.get_report_metadata().clear()
            else:
                log_debug("Clearing report extras.", contexts="report")
                Arjuna.get_report_metadata().clear()    
            
        except Exception as e:
            from arjuna import log_warning
            log_warning("Error in enhance_reports hook: " + str(e), contexts="report")
            raise


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
        from arjuna.tpi.engine.data_markup import record
        log_debug("{} {}".format(metafunc.function, metafunc.fixturenames), contexts="resource")

        group_params = Arjuna.get_group_params()
        conf = None
        m = metafunc.function.__module__
        group = record(**group_params).build(context='Group').all_records[0]
        log_debug("Parameterizing distributor for module: {} with group: {}".format(m, group), contexts="resource")
        metafunc.parametrize("group", argvalues=[group], ids=["G"], indirect=True)

    @classmethod
    def select_tests(cls, pytest_items, pytest_config):
        '''
            Select tests from items collected by pytest, based on Arjuna rules.

            Arguments:
                pytest_items: List of pytest `Item` objects. Each item represents a collected test function node.
                pytest_config: pytest Config object
        '''
        from arjuna import log_debug

        def process_nodename(item):
            return item.name.split("[")[0]

        from arjuna import Arjuna
        from arjuna.core.error import ExclusionRuleMet, NoInclusionRuleMet
        from arjuna import C
        selector = Arjuna.get_test_selector()
        final_selection = []
        deselected = []
        qual_names = set()

        for item in pytest_items:
            nid = item.nodeid
            log_debug(f"Processing {nid} as collected by pytest")
            # if item.name.split("[")[0] == "test":
            #     continue

            qual_name = None

            # For a test function
            # Root dir should be folder containing the module
            # E.g. check_config_03_create_conf.py::check_create_config[G]
            temp_full_path = os.path.join(pytest_config.rootdir, item.nodeid.split('::')[0])
            full_dotted_notation = temp_full_path.replace("/",".").replace('\\',".").replace(".py","") 
            full_dotted_notation =  full_dotted_notation.replace("..", ".")

            project_name = C("project.name")
            project_index = full_dotted_notation.find(project_name + "." + "test")

            if project_index == -1:
                deselected.append(item)
                continue

            qual_name = full_dotted_notation[project_index:] + "." + process_nodename(item)

            # if os.path.exists(temp_full_path):
            #     if os.path.isfile(temp_full_path):
            #         test_path_index = temp_full_path.find(os.path.join(C("project.root.dir"), "test"))
            #         if test_path_index == -1:
            #             continue
            #         else:
            #             dotted_root = str(pytest_config.rootdir).replace("/",".").replace('\\',"")
            #             proj_suffix = dotted_root[dotted_root.find(project_name):]
            #             qual_name = proj_suffix + "." + process_nodeid(item) + "." + process_nodename(item)
            # else:
            #     qual_name = process_nodeid(item) + "." + process_nodename(item)
            #     start_index = qual_name.find(project_name + "." + "test")
            #     if start_index == -1:
            #         if qual_name.startswith("test."):
            #             qual_name = project_name + "." + qual_name                    
            #         else:
            #             deselected.append(item)
            #             continue
            #     else:
            #         qual_name = qual_name[start_index:]

            try:
                selector.validate(Arjuna.get_test_meta_data(qual_name))
            except (ExclusionRuleMet, NoInclusionRuleMet) as e:
                deselected.append(item)
            else:
                final_selection.append(item)

        if deselected:
            pytest_config.hook.pytest_deselected(items=deselected)
            pytest_items[:] = final_selection


        