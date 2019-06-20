from .handler import Handler

class WebAlertHandler(Handler):

    def __init__(self, automator):
        super().__init__(automator)
        self.__alert_present = False
        self.__alert_setu_id = None
        self.__alert = None

    def create_alert(self):
        if self.__alert_present:
            return self.__alert
        else:
            self.wait()
            from arjuna.setuext.guiauto.impl.element.webalert import WebAlert
            self.__alert_present = True
            alert = WebAlert(self.automator)
            self.__alert_setu_id = alert.setu_id
            self.__alert = alert
            return alert

    def get_alert_for_setu_id(self, setu_id):
        msg = "The alert represented by this object no longer exists."
        if not self.__alert_present:
            raise Exception(msg)
        elif self.__alert_setu_id != setu_id:
            raise Exception(msg)
        else:
            return self.__alert

    def delete_alert(self):
        self.__alert_present = False
        self.__alert_setu_id = None
        self.__alert = None

    def wait(self):
        self.automator.conditions.AlertIsPresent().wait()

    def is_alert_present(self):
        return self.automator.dispatcher.is_web_alert_present()



