from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.enums import ArjunaOption

config = Arjuna.get_central_config().get_config()

wait_time = config.get_guiauto_max_wait_time();
print(wtime);

wait_value = config.get_arjuna_option_value(ArjunaOption.GUIAUTO_MAX_WAIT);
print(wait_value.as_int());

wait_value = config.get_arjuna_option_value("GUIAUTO_MAX_WAIT");
print(wait_value.as_int());

wait_value = config.get_arjuna_option_value("GuIAuTo_MaX_WaIt");
print(wait_value.as_int());

wait_value = config.get_arjuna_option_value("guiauto.max.wait");
print(wait_value.as_int());

wait_value = config.get_arjuna_option_value("guiauto.max.wait");
print(wait_value.as_int());

should_maximize_browser = config.getArjunaOptionValue(ArjunaOption.BROWSER_MAXIMIZE);
print(maxWaitValue.as_bool());
