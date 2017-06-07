package pvt.batteries.integration;

import java.util.ArrayList;

import pvt.arjunasdk.property.ConfigProperty;
import pvt.batteries.ds.MessagesContainer;
import pvt.batteries.ds.NamesContainer;
import pvt.batteries.hocon.HoconReader;
import pvt.batteries.lib.ComponentIntegrator;

public abstract class AbstractComponentConfigurator implements ComponentConfigurator {
	private String baseDir = null;
	private String componentName;
	private ComponentIntegrator integrator = null;

	public AbstractComponentConfigurator(String componentName) {
		this.setComponentName(componentName);
	}

	@Override
	public String getBaseDir() {
		return baseDir;
	}

	@Override
	public void setBaseDir(String dir) {
		this.baseDir = dir;
	}

	@Override
	public ComponentIntegrator getIntegrator() {
		return integrator;
	}

	@Override
	public void setIntegrator(ComponentIntegrator integrator) {
		this.integrator = integrator;
	}

	public String getComponentName() {
		return componentName;
	}

	private void setComponentName(String componentName) {
		this.componentName = componentName;
	}

	protected void registerProperty(ConfigProperty prop) throws Exception {
		integrator.registerProperty(this.getComponentName(), prop);
	}

	protected void processDefaults(HoconReader reader) throws Exception {
		reader.process();
		processConfigProperties(reader.getProperties());
		configureNames(getAllNames());
		configureMessages(getAllMessages());
	}

	protected abstract ArrayList<MessagesContainer> getAllMessages();

	protected abstract ArrayList<NamesContainer> getAllNames();

	public void configureMessages(ArrayList<MessagesContainer> messages) {
		this.integrator.populateMessages(messages);
	}

	public void configureNames(ArrayList<NamesContainer> names) {
		this.integrator.populateNames(names);
	}
}
