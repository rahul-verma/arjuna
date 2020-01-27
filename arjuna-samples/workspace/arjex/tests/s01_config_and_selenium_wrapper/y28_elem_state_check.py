from commons import *
from arjuna.tpi.guiauto.helpers import With, GuiActionConfig

init_arjuna()

narada = create_app()

url = narada.ui.config.get_user_option_value("narada.ex.elemstate.url").as_str()
narada.ui.browser.go_to_url(url)

narada.ui.element(With.id("target")).click()
narada.ui.alert.confirm()

narada.ui.browser.go_to_url(url)
conf = GuiActionConfig.builder().check_pre_state(False).build()
print(conf.settings)

narada.ui.element(With.id("target")).configure(conf).click()
narada.ui.alert.confirm()
