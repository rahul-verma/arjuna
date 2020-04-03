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

    @classmethod
    def get_request_attr(cls, item, obj_name):
        # This works. Now you have add a lookup.
        # Introduce concept of screen_shooter: any object with take_screenshot(prefix) signture of method.
        # print(type(item.module), item.module.app)
        from .test import Space
        request =  cls.get_request_obj(item)
        res = Space(request)
        return getattr(res, obj_name)

    @classmethod
    def get_request_obj(cls, item):
        return item.funcargs['request']

    @classmethod
    def get_plugin(cls, item, name):
        return item.config.pluginmanager.getplugin(name)

    @classmethod
    def get_html_report_plugin(cls, item):
        return cls.get_plugin(item, 'html')

    @classmethod
    def get_screen_shooter(cls, item):
        try:
            return getattr(item.function, "screen_shooter")
        except:
            return getattr(item.module, "screen_shooter")

    @classmethod
    def add_screenshot_for_result(cls, item, result, *, ignore_passed=True, ignore_fixtures=False):
        try:
            try:
                screen_shooter = cls.get_screen_shooter(item)
            except AttributeError:
                return
            html_plugin = cls.get_html_report_plugin(item)
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
                # extra.append(pytest_html.extras.url(app.base_url))


            import re
            rname = re.sub(r"\[.*?\]", "", report.nodeid)
            fpath, fb64 = screen_shooter.take_screenshot(prefix=rname)
            fpath = "../screenshot/{}".format(fpath)
            img_elem = '''<img src="data:image/png;base64,{}"/>'''.format(fb64)
            extra.append(
                pytest_html.extras.html(
                    '''<div class="image"><a href="{}" target="_blank">{}</a>'''.format(fpath, img_elem)
                )
            )
            report.extra = extra
        except Exception as e:
            print(e)