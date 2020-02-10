'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

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

class PytestHooks:


    @classmethod
    def get_request_attr(cls, item, obj_name):
        request =  cls.get_request_obj(item)
        return getattr(cls.get_container_based_on_scope(request), obj_name)

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
    def add_screenshot_for_failed_result(cls, html_plugin, outcome, *, screenshoter=None):
        pytest_html = html_plugin
        report = outcome.get_result()
        extra = getattr(report, 'extra', [])
        if report.when == 'call':

            xfail = hasattr(report, 'wasxfail')
            if (report.skipped and xfail) or (report.failed and not xfail):
                # extra.append(pytest_html.extras.url(app.base_url))
                fpath, fb64 = screenshoter.automator.take_screenshot()
                img_elem = '''<img src="data:image/png;base64,{}"/>'''.format(fb64)
                extra.append(
                    pytest_html.extras.html(
                        '''<div class="image"><a href="{}" target="_blank">{}</a>'''.format(fpath, img_elem)
                    )
                )
                report.extra = extra