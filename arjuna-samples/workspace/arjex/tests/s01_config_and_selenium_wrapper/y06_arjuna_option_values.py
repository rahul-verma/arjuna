from commons import *
from arjuna import *

init_arjuna()
config = Arjuna.get_ref_config()

wait_time = config.guiauto_max_wait_time
print(wait_time)

wait_value = config.get_arjuna_option_value(ArjunaOption.GUIAUTO_MAX_WAIT)
print(wait_value.as_int())

wait_value = config.get_arjuna_option_value("GUIAUTO_MAX_WAIT")
print(wait_value.as_int())

wait_value = config.get_arjuna_option_value("GuIAuTo_MaX_WaIt")
print(wait_value.as_int())

wait_value = config.get_arjuna_option_value("guiauto.max.wait")
print(wait_value.as_int())

wait_value = config.get_arjuna_option_value("guiauto.max.wait")
print(wait_value.as_int())

should_maximize_browser = config.get_arjuna_option_value(ArjunaOption.BROWSER_MAXIMIZE)
print(should_maximize_browser.as_bool())
