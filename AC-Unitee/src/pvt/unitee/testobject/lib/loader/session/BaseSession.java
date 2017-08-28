package pvt.unitee.testobject.lib.loader.session;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.apache.log4j.Logger;

import arjunasdk.config.RunConfig;
import pvt.batteries.value.DefaultStringKeyValueContainer;
import pvt.unitee.arjuna.TestGroupsDB;
import pvt.unitee.core.lib.exception.SessionNodesFinishedException;
import pvt.unitee.testobject.lib.java.processor.JavaTestClassDefProcessor;

public abstract class BaseSession implements Session {
	private static Logger logger = RunConfig.logger();
	private List<SessionNode> nodesQueue = new ArrayList<SessionNode>(); 
	private Iterator<SessionNode> iter = null;
	private int testMethodCount = 0;
	private String name = null;
	private DefaultStringKeyValueContainer execVars = new DefaultStringKeyValueContainer();
	private TestGroupsDB testGroupsDB = null;
	
	public BaseSession(String name) throws Exception{
		this.name = name;
		this.testGroupsDB = new TestGroupsDB(this);
	}
	
	@Override
	public void load() throws Exception{
		JavaTestClassDefProcessor processor = new JavaTestClassDefProcessor();
		processor.processMetaData();
		processor.processDependencies();
		logger.debug(String.format("%s: Loading nodes", this.getName()));
		for (SessionNode node: this.nodesQueue){
			logger.debug("Session Node: " + node.getName());
			node.load();
		}		
	}
	
	@Override
	public void schedule() throws Exception{
		logger.debug(String.format("%s: Scheduling nodes", this.getName()));
		for (SessionNode node: this.nodesQueue){
			logger.debug("Session Node: " + node.getName());
			node.schedule();
			this.testMethodCount += node.getTestMethodCount();
		}
		iter = nodesQueue.iterator();		
	}
	
	public void addNode(BaseSessionNode node){
		this.nodesQueue.add(node);
	}
	
	@Override
	public int getTestMethodCount() {
		return this.testMethodCount;
	}

	@Override
	public SessionNode next() throws Exception {
		if (iter.hasNext()){
			return iter.next();
		} else {
			throw new SessionNodesFinishedException();
		}
	}
	
	public String getName() {
		return this.name;
	}
	
	@Override
	public void setExecVars(DefaultStringKeyValueContainer execVars){
		this.execVars = execVars;
	}
	
	@Override 	
	public DefaultStringKeyValueContainer getExecVars(){
		return this.execVars;
	}
	
	@Override
	public boolean isDefaultSession(){
		return this.getName().toUpperCase().equals("MSESSION");
	}
	
	@Override
	public TestGroupsDB getGroupsDB() {
		return this.testGroupsDB;
	}
}