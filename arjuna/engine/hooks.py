

class PytestHooks:

    @classmethod
    def get_request_attr(cls, item, obj_name):
        request =  cls.get_request_obj(item)
        return getattr(request.cls, obj_name)

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