package pvt.unitee.testobject.lib.loader.group;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;

import pvt.batteries.config.Batteries;
import pvt.batteries.value.DefaultStringKeyValueContainer;
import pvt.unitee.runner.lib.slots.TestSlotExecutor;
import pvt.unitee.testobject.lib.loader.session.SessionNode;
import pvt.unitee.testobject.lib.loader.session.SessionSubNode;

public class BaseGroup implements Group{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private String sessionName = null;
	private String name = null;
	private TestLoader loader = null;
	private int classThreads = 1;
	List<Picker> containerPickers = null;
	private SessionSubNode sessionSubNode;
	private DefaultStringKeyValueContainer utvars = new DefaultStringKeyValueContainer();
	private Map<String,List<String>> classMethodMap = new HashMap<String,List<String>>();
	
	public BaseGroup(String name) throws Exception{
		this.name = name;
	}
	
	public BaseGroup(SessionSubNode node, String name) throws Exception{
		this.setSessionSubNode(node);
		this.name = name;
		this.utvars.cloneAdd(node.getUTV().items());
	}
	
	public void setGroupName(String name){
		this.name = name;
	}
	
	protected void setLoader(TestLoader loader){
		this.loader = loader;
	}

	public void load() throws Exception{
		logger.debug(String.format("%s: Loading containers", this.getName()));
		if (containerPickers != null){
			for (Picker picker: containerPickers){
				picker.setGroup(this);
			}
		}
		this.loader.load();
	}
	
	@Override
	public String getName() {
		return this.name;
	}

	@Override
	public TestSlotExecutor next() throws Exception {
		return loader.next();
	}

	@Override
	public int getTestMethodCount() {
		return this.loader.getTestMethodCount();
	}
	
	@Override
	public void setSessionName(String name) {
		this.sessionName = name;
	}
	
	@Override
	public String getSessionName() {
		return this.sessionName;
	}
	
	public void setClassThreadCount(int count) {
		this.classThreads = count;
	}
	
	public void setPickers(List<Picker> pickers) {
		this.containerPickers = pickers;
	}
	@Override
	public List<Picker> getPickers() {
		return this.containerPickers;
	}

	@Override
	public String getDefinitionFile() {
		return "NA";
	}

	public int getClassThreadCount() {
		return classThreads;
	}

	public SessionSubNode getSessionSubNode() {
		return sessionSubNode;
	}

	@Override
	public void setSessionSubNode(SessionSubNode sessionSubNode) {
		this.sessionSubNode = sessionSubNode;
	}

	@Override
	public DefaultStringKeyValueContainer getUTV() {
		return this.utvars;
	}

	@Override
	public SessionNode getSessionNode() {
		return this.sessionSubNode.getSessionNode();
	}

	@Override
	public void addClassMethodMap(String qualifiedName, List<String> scheduledCreators) {
		this.classMethodMap .put(qualifiedName, scheduledCreators);
	}

	@Override
	public List<String> getScheduledCreatorsForContainer(String qualifiedName) {
		return this.classMethodMap.get(qualifiedName);
	}
}
