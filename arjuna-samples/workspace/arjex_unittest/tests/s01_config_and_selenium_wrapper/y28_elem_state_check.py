from commons import *
from arjuna.tpi.guiauto.helpers import With, GuiActionConfig

init_arjuna()

automator = launch_automator()

url = automator.config.get_user_option_value("narada.ex.elemstate.url").as_str()
automator.browser.go_to_url(url)

automator.element(With.id("target")).click()
automator.alert.confirm()

automator.browser.go_to_url(url)
conf = GuiActionConfig.builder().check_pre_state(False).build()
print(conf.settings)

automator.element(With.id("target")).configure(conf).click()
automator.alert.confirm()
