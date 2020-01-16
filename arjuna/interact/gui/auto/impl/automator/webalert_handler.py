class WebAlertHandler:

    def __init__(self, automator):
        self.__automator = automator
        self.__alert_present = False
        self.__alert = None

    @property
    def automator(self):
        return self.__automator

    def create_alert(self):
        if self.__alert_present:
            return self.__alert
        else:
            self.wait()
            from arjuna.interact.gui.auto.impl.element.webalert import WebAlert
            self.__alert_present = True
            alert = WebAlert(self.automator)
            self.__alert = alert
            return alert

    def delete_alert(self):
        self.__alert_present = False
        self.__alert = None

    def wait(self):
        self.automator.conditions.AlertIsPresent().wait(max_wait_time=self.automator.config.get_arjuna_option_value("guiauto.max.wait").as_int())

    def is_alert_present(self):
        return self.automator.dispatcher.is_web_alert_present()



