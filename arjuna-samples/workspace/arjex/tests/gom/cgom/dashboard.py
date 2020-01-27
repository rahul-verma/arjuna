from .basepage import WPFullPage

class DashboardPage(WPFullPage):
    
    def __init__(self, app, automator):
        super().__init__(app, automator)