from arjuna.setuext.guiauto.dispatcher.automator import GuiAutomatorDispatcher

class TestSessionDispatcher:

    def create_gui_automator_dispatcher(self, config, setu_id):
        return GuiAutomatorDispatcher(config, setu_id)

    def create_gui_element_dispatcher(self, atuomator_dispatcher, element_setu_id):
        return atuomator_dispatcher.create_gui_element_dispatcher(element_setu_id)
