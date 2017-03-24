package pvt.batteries.hocon;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map.Entry;

import org.apache.poi.util.SystemOutLogger;

import java.util.Set;

import com.arjunapro.testauto.interfaces.Value;
import com.typesafe.config.Config;
import com.typesafe.config.ConfigFactory;
import com.typesafe.config.ConfigParseOptions;
import com.typesafe.config.ConfigResolveOptions;
import com.typesafe.config.ConfigSyntax;
import com.typesafe.config.ConfigValue;

import pvt.arjunapro.enums.HoconSyntaxType;
import pvt.batteries.value.AnyRefListValue;
import pvt.batteries.value.AnyRefValue;
import pvt.batteries.value.BooleanValue;
import pvt.batteries.value.NullValue;
import pvt.batteries.value.NumberValue;
import pvt.batteries.value.StringValue;

public abstract class AbstractHoconReader implements HoconReader {
	private HashMap<String, Value> map = new HashMap<String, Value>();
	private static Set<Entry<String, ConfigValue>> systemSet = null;
	private static Set<String> systemKeys = new HashSet<String>();
	private Config loadedConf = null;
	ConfigParseOptions parseOptions = null;
	ConfigResolveOptions resolveOptions = null;

	public AbstractHoconReader() {
		this(ConfigParseOptions.defaults().setSyntax(ConfigSyntax.CONF), ConfigResolveOptions.noSystem());
	}

	public AbstractHoconReader(HoconSyntaxType parseSyntax) {
		this(ConfigParseOptions.defaults().setSyntax(ConfigSyntax.valueOf(parseSyntax.toString())),
				ConfigResolveOptions.noSystem());
	}

	public Set<Entry<String, ConfigValue>> getSystemPropSet(){
		return systemSet;
	}
	

	private void populatesysProps(){
		if (systemSet == null) {
			systemSet = ConfigFactory.systemProperties().entrySet();
			Iterator<Entry<String, ConfigValue>> iter = systemSet.iterator();
			while(iter.hasNext()){
				Entry<String, ConfigValue> v = iter.next();
				systemKeys.add(v.getKey());
			}
		}		
	}
	
	@Override
	public Set<String> getSystemKeys() {
		return systemKeys;
	}
	
	private AbstractHoconReader(ConfigParseOptions parseOptions, ConfigResolveOptions resolveOptions) {
		populatesysProps();
		this.parseOptions = parseOptions;
		this.resolveOptions = resolveOptions;
	}

	protected ConfigParseOptions getParseOptions() {
		return this.parseOptions;
	}

	protected ConfigResolveOptions getResolveOptions() {
		return this.resolveOptions;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.batteries.config.HoconReader#setConfig(com.typesafe.
	 * config.Config)
	 */
	@Override
	public void setConfig(Config loadedConf) {
		this.loadedConf = loadedConf;
	}

	public abstract void loadConfig() throws Exception;

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.batteries.config.HoconReader#process()
	 */
	@Override
	public void process() throws Exception {
		loadConfig();
		Set<Entry<String, ConfigValue>> bConf = loadedConf.entrySet();
		bConf.removeAll(systemSet);

		Iterator<Entry<String, ConfigValue>> iter = bConf.iterator();

		while (iter.hasNext()) {
			Entry<String, ConfigValue> entry = iter.next();
//			System.out.println(entry);
//			System.out.println(entry.getValue().valueType());
			switch (entry.getValue().valueType()) {
			case BOOLEAN:
				map.put(entry.getKey(), new BooleanValue((boolean) entry.getValue().unwrapped()));
				break;
			case LIST:
				map.put(entry.getKey(), new AnyRefListValue((List) entry.getValue().unwrapped()));
				break;
			case NULL:
				map.put(entry.getKey(), new NullValue());
				break;
			case NUMBER:
				map.put(entry.getKey(), new NumberValue((Number) entry.getValue().unwrapped()));
				break;
			case OBJECT:
				map.put(entry.getKey(), new AnyRefValue(entry.getValue().unwrapped()));
				break;
			case STRING:
				map.put(entry.getKey(), new StringValue((String) entry.getValue().unwrapped()));
				break;
			default:
				break;

			}
		}
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.batteries.config.HoconReader#getConfig()
	 */
	@Override
	public Config getConfig() {
		return this.loadedConf;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.batteries.config.HoconReader#getProperties()
	 */
	@Override
	public HashMap<String, Value> getProperties() {
		return map;
	}
}
