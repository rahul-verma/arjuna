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
from py.xml import html, raw

ARJUNA_JS = '''
function openModal(event){
    var source = event.target || event.srcElement;
    var modal = document.getElementById("modal-packet");
    modal.style.display = "block";
    var req = document.getElementById("modal-packet-request");
    req.innerHTML = ""
    var h3_req = document.createElement("h3");
    h3_req.innerHTML = "Request"
    req.appendChild(h3_req)
    req.appendChild(document.createTextNode(source.getAttribute("data-request")))

    var res = document.getElementById("modal-packet-response");
    res.innerHTML = ""
    var h3_res = document.createElement("h3");
    h3_res.innerHTML = "Response"
    req.appendChild(h3_res)
    res.appendChild(document.createTextNode(source.getAttribute("data-response")))
    var span = document.getElementById(source.id + "modal-packet-span");
    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

}

function openModalImage(event){
    var img_link = event.target || event.srcElement;
    var modal = document.getElementById("modal-image");
    var modal_image = document.getElementById("modal-image-content");
    modal.style.display = "block";
    modal_image.src = img_link.src;
    var span = document.getElementById("modal-image-span");
    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}
'''

IMG_SPAN ='''

<!-- The Network Packet Modal -->
<div id="modal-packet" class="modal">

  <!-- Modal content -->
  <div class="modal-content">
    <span id="modal-packet-span" class="close">&times;</span>
    <div class="linebreaks"><p id="modal-packet-request"></p><p id="modal-packet-response"></p>
    </div>
  </div>

</div>

<!-- The Modal -->
<div id="modal-image" class="modal">
<div class="modal-content">
  <span id="modal-image-span" class="close">&times;</span>
  <img id="modal-image-content" class="modal-content">
  <div id="caption"></div>
  </div>
</div>
'''

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
        prefix += [html.script(raw(ARJUNA_JS))]
        prefix += [raw(IMG_SPAN)]

    @classmethod
    def enhance_reports(cls, item, result, *, ignore_passed=True, ignore_fixtures=False):
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
            html_plugin = cls._get_html_report_plugin(item)
            pytest_html = html_plugin
            report = result.get_result()
            extra = getattr(report, 'extra', [])

            # if ignore_fixtures:
            #     if report.when == 'call':
            #         return

            xfail = hasattr(report, 'wasxfail')

            if ignore_passed and report.passed:
                pass
            else:
                # if (report.skipped and xfail) and (report.failed and not xfail):
                    # extra.append(pytest_html.extras.url(app.url))
                try:
                    screen_shooter = cls._get_screen_shooter(item)
                except AttributeError:
                    pass
                else:
                    screen_shooter.take_screenshot(prefix=report.nodeid)
            
            from arjuna import Arjuna
            test_container = Arjuna.get_report_metadata()
            if test_container.has_content():
                extra.append(pytest_html.extras.html(test_container.as_report_html()))

            # For fixtures with errors, failures, clean the resources.
            if report.when in {"setup", "teardown"}:
                if not report.passed:
                    Arjuna.get_report_metadata().clear()
            else:
                Arjuna.get_report_metadata().clear()
            
            report.extra = extra
        except Exception as e:
            raise
            from arjuna import log_warning
            log_warning("Error in enhance_reports hook: " + str(e))


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


        